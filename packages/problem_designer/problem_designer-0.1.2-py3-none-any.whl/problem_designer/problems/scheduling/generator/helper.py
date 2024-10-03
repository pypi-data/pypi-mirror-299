import math
import uuid
from dataclasses import dataclass

from problem_designer.problems.scheduling.constants.characteristic import (
    DemandsCharacteristics,
    ProcessingTimeCharacteristic,
    TransportationTimeCharacteristic,
)
from problem_designer.problems.scheduling.constants.objective import SupportedObjectives
from problem_designer.problems.scheduling.generator.typedef import (
    GeneratorStep,
    IntermediateGeneratedProblem,
)


@dataclass
class GenerateFixedNumberOfTasksPerJob(GeneratorStep):
    """
    Generates a mapping for a job containing a fixed number of tasks
    """

    number_of_jobs: int
    number_of_tasks_per_job: int

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        task_cnt = 0
        all_tasks = {}
        for _ in range(self.number_of_jobs):
            job_uuid = str(uuid.uuid4())  # create new job id
            tasks = []
            for _ in range(self.number_of_tasks_per_job):
                task_uuid = str(uuid.uuid4())  # create new task id
                tasks.append(task_uuid)
                all_tasks[task_cnt] = task_uuid
                task_cnt += 1
            igp.map_job_to_tasks[job_uuid] = tasks
        igp.total_number_of_tasks = sum(len(tasks) for tasks in igp.map_job_to_tasks.values())
        igp.number_of_jobs = self.number_of_jobs
        igp.tasks = all_tasks
        return igp


@dataclass
class GenerateAmountOfStages(GeneratorStep):
    """
    Generates the amount of stages
    """

    number_of_stages: int

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.number_of_stages = self.number_of_stages
        return igp


@dataclass
class GenerateFixedIndexMappingToMachine(GeneratorStep):
    """
    Generates a fixed mapping from the ith task to the ith machine
    """

    number_of_machines: int

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.map_machine_to_tasks = None
        igp.number_of_machines = self.number_of_machines

        # create machines
        for m in range(igp.number_of_machines):
            igp.machines[m] = str(uuid.uuid4())
        return igp


@dataclass
class GenerateFixedIndexMappingFromStageToMachine(GeneratorStep):
    """
    Generates a fixed mapping from a stage to its corresponding machines.
    """

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.number_of_machines_per_stage = int(igp.number_of_machines / igp.number_of_stages)

        for stage in range(igp.number_of_stages):
            machine_list = []
            for _ in range(igp.number_of_machines_per_stage):
                machine_uuid = str(uuid.uuid4())
                machine_list.append(machine_uuid)
            igp.map_stage_to_machines[str(stage)] = machine_list
        return igp


@dataclass
class GenerateProcessingTimes(GeneratorStep):
    """
    Generates processing times according to a distribution mapped to corresponding job.
    """

    pt: ProcessingTimeCharacteristic

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        for job_uuid, tasks in igp.map_job_to_tasks.items():
            igp.job_to_processing_times[job_uuid] = self.pt.distribution.take_n(n=len(tasks))
        return igp


@dataclass
class GenerateTransportationTimesForMachinesWithStages(GeneratorStep):
    """
    Generates random transportation times between two machines at two different stages
    according to a distribution.
    <br/>The machines of the last stage do not have any transportation time
    as there are no further machines left to be visited.
    Therefore its value is null.
    """

    tt: TransportationTimeCharacteristic

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        for stage, machines in igp.map_stage_to_machines.items():
            for machine in machines:
                next_stage_dict = {}
                next_stage = int(stage) + 1
                # check if next stage exists
                if next_stage < len(igp.map_stage_to_machines):
                    next_stage_machines = igp.map_stage_to_machines[str(next_stage)]
                    for next_machine in next_stage_machines:
                        next_stage_dict[next_machine] = self.tt.distribution.get_random_value()
                else:
                    next_stage_dict = None
                igp.machine_to_transportation_times[machine] = next_stage_dict
        return igp


@dataclass
class GenerateTransportationTimes(GeneratorStep):
    """
    Generates transportation times between two machines according to a distribution
    """

    tt: TransportationTimeCharacteristic

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        dict_of_dicts = {}
        for from_machine in igp.machines.values():
            machine_to_trans_time = {}
            for to_machine in igp.machines.values():
                machine_to_trans_time[to_machine] = self.tt.distribution.get_random_value()
            dict_of_dicts[from_machine] = machine_to_trans_time
        igp.machine_to_transportation_times = dict_of_dicts
        return igp


@dataclass
class GenerateMachineCapacities(GeneratorStep):
    """
    Generates capacities for every machine for given time stamps.
    If no value for capacity is given, default value 1 is taken.<br/>
    Dictionary structure: { "machine_uuid": { "time_stamp": capacity } }
    """

    cap: dict[str, dict[str, int]]
    default_cap: int | dict[str, int]

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        # Handle user defined capacities
        igp.machine_capacity = {
            # Map each machine UUID to its corresponding capacity from self.cap.
            # If a machine index is not found in self.cap, assign an empty dictionary as its capacity.
            machine_id: self.cap.get(str(idx), {})
            for idx, machine_id in igp.machines.items()
        }

        # Handle default capacities
        if isinstance(self.default_cap, int):
            # Set default capacities for all machines to the same value
            igp.default_capacities = {machine_id: self.default_cap for machine_id in igp.machines.values()}
        elif isinstance(self.default_cap, dict):
            # Convert machine indices from user input file to UUIDs and map capacities
            igp.default_capacities = {
                machine_id: self.default_cap.get(str(idx), 1) for idx, machine_id in igp.machines.items()
            }
        return igp


@dataclass
class GenerateDemands(GeneratorStep):
    """
    Generates capacity and energy demands according to a distribution.<br/>
    Dictionary structure: { "task_id": { "demand_type": value } }
    """

    dc: DemandsCharacteristics

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        for task_uuid in igp.tasks.values():
            energy_demand = self.dc.distribution.take_one()
            igp.demands_per_task[task_uuid] = {
                "capacity_demand": 1,
                "energy_demand": int(math.ceil(energy_demand / 100)) * 100,  # round up to next 100
            }
        return igp


@dataclass
class GenerateObjectives(GeneratorStep):
    objectives: list[SupportedObjectives]

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.objectives = [o.type for o in self.objectives]
        return igp
