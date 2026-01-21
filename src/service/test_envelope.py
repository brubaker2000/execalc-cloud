from src.service.envelope import IngressEnvelope


def test_ingress_envelope_defaults():
    env = IngressEnvelope(input={"hello": "world"})

    assert env.input == {"hello": "world"}
    assert env.tenant_context is None
    assert env.meta == {}
    assert env.mutable is True
