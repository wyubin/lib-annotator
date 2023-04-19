# intro
提供在 python 環境中能夠方便地進行 生物資料庫的 annotation 的 package, 目前以 varNote 為主要核心。

# requirement
- Python >= 3.7
- JRE >= 8.0

# install
```shell
python3 -m pip install git+https://github.com/wyubin/lib-annotator.git#egg=annotator
```

# usage
- 安裝好 `annotator` 後，可在 python 環境中使用，如下
```python
from annotator import Annotator

conf = {
    'hg19': '/root/taigenomics-staging/volume/pub/hg19.resource/1/Annotator',
    'hg38': '/root/taigenomics-staging/volume/pub/hg38.resource/1/Annotator'
}

anno = Annotator(conf)  # setup path, hg19/hg38/varnote jar
proc = anno.get_processor('ClinVar', 'hg19')  # return processor self
path_proj = Path('/root/taigenomics-staging/volume/yubin/dev-test/hg38_dev.sample/2')
path_input = path_proj.joinpath('hg38-dev.decomposed.normalized.vcf')
path_output = path_proj.joinpath('test_annotator.vcf')

return_code = proc.run(input=path_input, output=path_output) # pid can be accessed from proc.processor.pid
```
