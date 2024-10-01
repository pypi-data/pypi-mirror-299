from pydantic import BaseModel


class GpuProcessor(BaseModel):

    gpu_id: int
