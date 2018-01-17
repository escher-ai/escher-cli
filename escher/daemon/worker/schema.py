import graphene
from escher_cli import local_runner, runner

from escher_cli.escher import run


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                           #
#          make sure you make this as thin as possible.                                     #
#                                                                                           #
#          Use this as a *thin* wrapper around the `cli` module.                            #
#                                                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

### Types
class Job(graphene.ObjectType):
    pid = graphene.String()
    status = graphene.String()


### Mutations
class StartJob(graphene.Mutation):
    class Input:
        work_directory = graphene.String()
        config_file = graphene.String()

    pid = graphene.String()

    def mutate(self, args, context, info):
        runner.run(args.get('config_file'), args.get('work_directory'))
        return StartJob(pid=args.get('name'))


class HaltJob(graphene.Mutation):
    class Input:
        name = graphene.String()

    pid = graphene.String()

    def mutate(self, args, context, info):
        return HaltJob(pid=args.get('name'))


class ResumeJob(graphene.Mutation):
    class Input:
        name = graphene.String()

    pid = graphene.String()

    def mutate(self, args, context, info):
        return ResumeJob(pid=args.get('name'))


class RerunJob(graphene.Mutation):
    class Input:
        name = graphene.String()

    pid = graphene.String()

    def mutate(self, args, context, info):
        return RerunJob(pid=args.get('name'))


class Mutations(graphene.ObjectType):
    start_job = StartJob.Field()
    halt_job = HaltJob.Field()
    resume_job = ResumeJob.Field()
    rerun_job = RerunJob.Field()


### Queries
class Query(graphene.ObjectType):
    running = graphene.List(lambda: Job).Field()

    def resolve_running(self, *args):
        """todo: queries local folder /tmp/escher/"""
        return [Job(pid="some")] * 5


schema = graphene.Schema(query=Query, mutation=Mutations)
