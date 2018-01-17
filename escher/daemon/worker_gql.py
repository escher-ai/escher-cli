import graphene


### Mutations
class StartJob(graphene.Mutation):
    class Input:
        name = graphene.String()

    name = graphene.String()

    def mutate(self, args, context, info):
        return StartJob(name=args.get('name'))


class HaltJob(graphene.Mutation):
    class Arguments:
        pass

    def mutate(self, info, name):
        return HaltJob(*args)


class ResumeJob(graphene.Mutation):
    class Arguments:
        pass

    def mutate(self, info, *args):
        return ResumeJob(*args)


class TerminateJob(graphene.Mutation):
    class Arguments:
        pass

    def mutate(self, info, *args):
        return TerminateJob(*args)


class Job(graphene.ObjectType):
    pid = graphene.String()
    # status = graphene.String()


class Mutations(graphene.ObjectType):
    start_job = StartJob.Field()
    # halt_job = HaltJob.Field()
    # terminate_job = TerminateJob.Field()


# We must define a query for our schema
class Query(graphene.ObjectType):
    running = graphene.List(lambda: Job).Field()

    def resolve_running(self, *args):
        """todo: queries local folder /tmp/escher/"""
        return [Job(pid="some")] * 5


schema = graphene.Schema(query=Query, mutation=Mutations)
