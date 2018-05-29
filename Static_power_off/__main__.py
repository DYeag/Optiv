import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_helpers
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.teardown.default_teardown_orchestrator import DefaultTeardownWorkflow


def main():
    sandbox = Sandbox()
    #session = script_helpers.get_api_session()
    #sandbox_id = script_helpers.get_reservation_context_details().id
    #sandbox_resources = session.GetReservationDetails(sandbox_id).ReservationDescription.Resources
    sandbox_resources = sandbox.automation_api.GetReservationDetails(sandbox.id).ReservationDescription.Resources
    static_vms = [res for res in sandbox_resources if (res.ResourceModelName == 'vCenter Static VM' and sandbox.automation_api.GetAttributeValue(res.Name, 'Auto Power Off').Value)]
    if static_vms.__len__() > 0:
        for static_vm in static_vms:
            #sandbox.automation_api.ExecuteResourceConnectedCommand(
            #    reservationId=sandbox.id,
            #    resourceFullPath=static_vm.Name,
            #    commandName='remote_restore_snapshot',
            #    commandTag='connectivity',
            #    parameterValues=['default'],
            #    printOutput=True
            #)
            sandbox.automation_api.ExecuteResourceConnectedCommand(
                reservationId=sandbox.id,
                resourceFullPath=static_vm.Name,
                commandName='PowerOff',
                commandTag='power',
                parameterValues=[],
                printOutput=True
            )
    else:
        sandbox.automation_api.WriteMessageToReservationOutput(
            reservationId=sandbox.id,
            message='No Static VMs to turn off!'
        )
    #sandbox = Sandbox()
    DefaultTeardownWorkflow().register(sandbox)
    sandbox.execute_teardown()


if __name__ == "__main__":
    main()
