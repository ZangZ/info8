from qiniu import Auth, put_data

access_key = "84GPGTqGIIgRA6N72fuSEp7oqSn_tJTY_Iqgz0UB"
secret_key = "7eGge9bJVssjH2CaGHu2w6Dckd1C4hdEWGO_qmT8"
bucket_name = "zanguncle"

# TODO access_key 和 bucket_name 不能用


def storage(data):
    try:
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = put_data(token, None, data)
        print(ret, info)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传图片失败")
    return ret["key"]


if __name__ == '__main__':
    file = input('请输入文件路径')
    with open(file, 'rb') as f:
        storage(f.read())