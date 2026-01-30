import time, logging
from ami_client.operation.event import (
    Event,
    AgentConnect, AgentComplete,
    QueueCallerJoin, QueueCallerAbandon,
    VarSet, Newexten,
)
from application.connections import ami_client, cti_client
from ._base import Job

logger = logging.getLogger('ami_to_cti')


ami_client.add_blacklist([VarSet, Newexten])

@ami_client.on_event(Event)
def on_all_events(event: Event):
    logger.debug(f'New event: {event.to_dict}')


@ami_client.on_event(QueueCallerJoin)  #type: ignore
def on_caller_join(event: QueueCallerJoin):
    if not event.Queue == '501':
        return
    print(event.to_dict())

    _from = event.CallerIDNum
    to = event.Queue
    direction = 'in'
    call_id = f'{event.Queue}.{event.Uniqueid}'

    if _from and to and direction and call_id:
        cti_client.new_call(
            _from=_from,
            to=to,
            direction=direction,
            call_id=call_id,
        )
    else:
        logger.debug(f'invalid data to send to zammadCTI: {_from=} {to=} {direction=} {call_id=}')


@ami_client.on_event(AgentConnect)  #type: ignore
def on_agent_connect(event: AgentConnect):
    if not event.Queue == '501':
        return

    _from = event.CallerIDNum
    to = event.Queue
    direction = 'in'
    user = event.MemberName
    call_id = f'{event.Queue}.{event.Uniqueid}'

    if _from and to and direction and call_id:
        cti_client.answer(
            _from=_from,
            to=to,
            direction=direction,
            user=user,
            call_id=call_id,
        )
    else:
        logger.debug(f'invalid data to send to zammadCTI: {_from=} {to=} {direction=} {call_id=} {user=}')


@ami_client.on_event(AgentComplete)  #type: ignore
def on_agent_complete(event: AgentComplete):
    if not event.Queue == '501':
        return

    _from = event.CallerIDNum
    to = event.Queue
    direction = 'in'
    call_id = f'{event.Queue}.{event.Uniqueid}'

    if _from and to and direction and call_id:
        cti_client.hangup(
            _from=_from,
            to=to,
            direction=direction,
            call_id=call_id,
            cause='normalClearing',
        )
    else:
        logger.debug(f'invalid data to send to zammadCTI: {_from=} {to=} {direction=} {call_id=}')


@ami_client.on_event(QueueCallerAbandon)  #type: ignore
def on_caller_abandon(event: QueueCallerAbandon):
    if not event.Queue == '501':
        return

    _from = event.CallerIDNum
    to = event.Queue
    direction = 'in'
    call_id = f'{event.Queue}.{event.Uniqueid}'

    if _from and to and direction and call_id:
        cti_client.hangup(
            _from=_from,
            to=to,
            direction=direction,
            call_id=call_id,
            cause='cancel',
        )
    else:
        logger.debug(f'invalid data to send to zammadCTI: {_from=} {to=} {direction=} {call_id=}')



class AMIToCTI(Job):
    def run(self) -> None:
        with ami_client:
            while not self.stop_event.is_set():
                if not ami_client.is_connected():
                    ami_client.connect()
                    ami_client.login()

                time.sleep(5)
