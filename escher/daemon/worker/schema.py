import graphene


### Types
class Job(graphene.ObjectType):
    pid = graphene.String()
    status = graphene.String()


### Mutations
class StartJob(graphene.Mutation):
    class Input:
        name = graphene.String()

    pid = graphene.String()

    def mutate(self, args, context, info):
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


class Mutations(graphene.ObjectType):
    start_job = StartJob.Field()
    halt_job = HaltJob.Field()
    resume_job = ResumeJob.Field()


### Queries
class Query(graphene.ObjectType):
    running = graphene.List(lambda: Job).Field()

    def resolve_running(self, *args):
        """todo: queries local folder /tmp/escher/"""
        return [Job(pid="some")] * 5


schema = graphene.Schema(query=Query, mutation=Mutations)
