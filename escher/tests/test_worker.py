from escher.daemon.worker.schema import schema


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


def test_start_job():
    # todo: get this to work. fix path.
    result = schema.execute("""
    mutation {
        startJob (
            configFile:"scripts/test.escher",
            workDirectory: "../../test_project"
        ) {
            pid
        }
    }""")
    print(result.data)
    print(result.errors)


def test_halt_job():
    result = schema.execute("""
    mutation {
        haltJob (name:"Peter") {
            name
        }
    }""")
    print(result.data)


def test_resume_job():
    result = schema.execute("""
    mutation {
        resumeJob (name:"Peter") {
            name
        }
    }""")
    print(result.data)


def test_rerun_job():
    result = schema.execute("""
    mutation {
        rerunJob (name:"Peter") {
            name
        }
    }""")
    print(result.data)
