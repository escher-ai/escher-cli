import graphene


class Master(graphene.ObjectType):
    id = graphene.String()
    uri = graphene.String()
    queue = graphene.String()


class Worker(graphene.ObjectType):
    id = graphene.String()
    ip = graphene.String()
    jobs = graphene.List


class Queue(graphene.ObjectType):
    id = graphene.String()
    worker = graphene.String()


class Job(graphene.ObjectType):
    id = graphene.String()
    backend = graphene.String()
    status = graphene.String()  # running, complete, halt


class initMaster(graphene.Mutation):
    class Arguments:
        id = graphene.String
        ip = graphene.String
        port = graphene.String

    id = graphene.String
    ip = graphene.String
    port = graphene.String

    def mutation(self, info, **args):
        return initMaster(**args)
