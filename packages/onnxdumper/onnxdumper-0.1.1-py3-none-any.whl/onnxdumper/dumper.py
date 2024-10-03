import datetime
import os
import onnx
import onnxruntime

class InferenceSession(onnxruntime.InferenceSession):
    def __init__(
        self,
        path_or_bytes: str | bytes | os.PathLike,
        **kwargs,
    ) -> None:
        # 创建影子Session
        self.model=onnx.load(path_or_bytes)
        # 修改模型输出节点tag
        for node in self.model.graph.node:
            for output in node.output:
                self.model.graph.output.extend([onnx.ValueInfoProto(name=output)])
        self.ShadowSession = onnxruntime.InferenceSession(self.model.SerializeToString())
        super().__init__(path_or_bytes, **kwargs)

    def run(self, output_names, input_feed, run_options=None):
        # 调用父类的run方法
        results = super().run(output_names, input_feed, run_options)
        # 调用影子Session的run方法
        self.ShadowSession.run(output_names, input_feed, run_options)
        outputs = [x.name for x in self.ShadowSession.get_outputs()]
        # 生成字典，便于查找层对应输出
        ort_outs = zip(outputs, ort_outs)
        # json格式写出到一个文件
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_name=f"{self.model.graph.name}_{date}.txt"
        with open(file_name, "w") as f:
            f.write(str(ort_outs))
        return results