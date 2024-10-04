from setuptools import setup, find_packages

setup(
    name="TracingLib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'opentelemetry-api',
        'opentelemetry-sdk',
        'opentelemetry-exporter-otlp'
    ],
    description="A package to manage OpenTelemetry tracing, spans, and events.",
    author="Rahul Singh Chauhan",
    author_email="chauhan.rahul2605@gmail.com",
)

