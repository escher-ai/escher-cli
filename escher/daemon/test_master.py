from escher.daemon.worker_gql import schema


def test_schema():
    result = schema.execute("""
    {
        __schema {mutationType{name}}
    } """)
    print(result.errors) if result.errors else print(result.data)


def test_running():
    result = schema.execute("""{
        running {pid}
    } """)
    assert result.data['running'] is not None, "todo: should be a list of fake jobs"

    result = schema.execute("""
    mutation myFirstMutation {
        startJob (name:"Peter") {
            name
        }
    }""")
    print(result.data)
    # assert result.data['startJob'] is not None, "createPerson field should exist"

    # result = schema.execute("""
    #     mutation {
    #     jobComplete() {
    #         id
    #         worker
    #         logDirectory
    #     }
    # } """)
    # assert result.data['stopJob'] is not None, "createPerson field should exist"
    #
    # result = schema.execute("""
    #     mutation {
    #     terminate() {
    #         ok
    #     }
    # } """)
    # assert result.data['stopJob'] is not None, "createPerson field should exist"
