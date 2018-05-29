import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_helpers
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox


def main():
    sandbox = Sandbox()
    #session = script_helpers.get_api_session()
    #sandbox_id = script_helpers.get_reservation_context_details().id
    #sandbox_resources = session.GetReservationDetails(sandbox_id).ReservationDescription.Resources
    sandbox_resources = sandbox.automation_api.GetReservationDetails(sandbox.id).ReservationDescription.Resources
    static_vms = [res for res in sandbox_resources if res.ResourceModelName == 'vCenter Static VM']
    if static_vms.__len__() > 0:
        for static_vm in static_vms:
            sandbox.automation_api.ExecuteResourceConnectedCommand(
                reservationId=sandbox.id,
                resourceFullPath=static_vm.Name,
                commandName='PowerOn',
                commandTag='power',
                parameterValues=[],
                printOutput=True
            )
    else:
        session.WriteMessageToReservationOutput(
            reservationId=sandbox.id,
            message='No Static VMs to turn on!'
        )
    #sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox)
    sandbox.execute_setup()


if __name__ == "__main__":
    main()
