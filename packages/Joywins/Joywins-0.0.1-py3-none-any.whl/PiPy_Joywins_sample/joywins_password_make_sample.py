""" 

### 15.파이썬 패키지 만들어 PyPI 에 등록하기 : 

## 참조 자료 : 
### URL : [파이썬 Python 코딩 - 패키지 만들어서 PyPI에 등록하기, 파이썬 저장소에 소스코드 등록, 개발자 인증^^ - YouTube | 나이스코딩](https://www.youtube.com/watch?v=UogEmMXR8HA)
### URL : [python_example/password_make.py at main · nicecoding1/python_example | 파이썬 Python 코딩 - 패키지 만들어서 PyPI에 등록하기, 파이썬 저장소에 소스코드 등록, 개발자 인증^^ - YouTube | 나이스코딩](https://github.com/nicecoding1/python_example/blob/main/password_make.py)


## 개발환경 

- PyPI 에 등록  라이브러리 설치 :
```
pip install setuptools wheel
```

#### 실습 파일 : 
- 예시 파일 : C:\Joywins\TechArchive\TechArchive_GoogleSpreadsheet\Ex031_pypi_nicecoding_sample\Ex031_pypi_nicecoding_password_make_sample.py

"""

import random

def password_make(length):
    a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@$%^&*()."
    b = list(a)
    pw = ""
    
    random.shuffle(b)

    try:
        for i in range(length):
            pw += str(b.pop())
    
    except Exception as e:
        print(e)
    
    return pw


if __name__ == "__main__":
    pw = password_make(12)
    print(pw)