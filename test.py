import requests
import json
import time

# 服务基础 URL
BASE_URL = "http://localhost:9999"

print("=== Deepseek API 服务测试 ===")
print(f"测试服务地址: {BASE_URL}")
print("==============================\n")

# 测试 1: 健康检查
def test_health():
    print("测试 1: 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ 健康检查成功: {response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败: 状态码 {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {str(e)}")
        return False

# 测试 2: 获取模型列表
def test_models():
    print("\n测试 2: 获取模型列表")
    try:
        response = requests.get(f"{BASE_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ 模型列表获取成功，共 {len(models)} 个模型:")
            for model in models:
                print(f"  - {model.get('name')}")
            return True
        else:
            print(f"❌ 模型列表获取失败: 状态码 {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 模型列表获取异常: {str(e)}")
        return False

# 测试 3: 获取版本信息
def test_version():
    print("\n测试 3: 获取版本信息")
    try:
        response = requests.get(f"{BASE_URL}/api/version")
        if response.status_code == 200:
            print(f"✅ 版本信息获取成功: {response.json()}")
            return True
        else:
            print(f"❌ 版本信息获取失败: 状态码 {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 版本信息获取异常: {str(e)}")
        return False

# 测试 4: OpenAI 兼容接口（非流式）
def test_openai_chat():
    print("\n测试 4: OpenAI 兼容接口（非流式）")
    try:
        payload = {
            "model": "deepseek_v3",
            "messages": [
                {"role": "system", "content": "你是一个智能助手"},
                {"role": "user", "content": "你好，简单介绍一下自己"}
            ],
            "stream": False
        }
        
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ OpenAI 兼容接口测试成功")
            print(f"  响应时间: {end_time - start_time:.2f} 秒")
            print(f"  模型: {data.get('model')}")
            print(f"  响应内容: {content[:100]}..." if len(content) > 100 else f"  响应内容: {content}")
            return True
        else:
            print(f"❌ OpenAI 兼容接口测试失败: 状态码 {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ OpenAI 兼容接口测试异常: {str(e)}")
        return False

# 测试 5: API 生成接口
def test_generate():
    print("\n测试 5: API 生成接口")
    try:
        payload = {
            "model": "deepseek_v3",
            "prompt": "简单介绍一下人工智能",
            "stream": False
        }
        
        response = requests.post(f"{BASE_URL}/api/generate", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API 生成接口测试成功")
            print(f"  模型: {data.get('model')}")
            print(f"  响应内容: {data.get('response', '')[:100]}..." if len(data.get('response', '')) > 100 else f"  响应内容: {data.get('response', '')}")
            return True
        else:
            print(f"❌ API 生成接口测试失败: 状态码 {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API 生成接口测试异常: {str(e)}")
        return False

# 测试 6: API 聊天接口
def test_chat():
    print("\n测试 6: API 聊天接口")
    try:
        payload = {
            "model": "deepseek_v3",
            "messages": [
                {"role": "system", "content": "你是一个智能助手"},
                {"role": "user", "content": "什么是机器学习？"}
            ]
        }
        
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "")
            print(f"✅ API 聊天接口测试成功")
            print(f"  模型: {data.get('model')}")
            print(f"  响应内容: {content[:100]}..." if len(content) > 100 else f"  响应内容: {content}")
            return True
        else:
            print(f"❌ API 聊天接口测试失败: 状态码 {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API 聊天接口测试异常: {str(e)}")
        return False

# 主测试函数
def run_tests():
    print("开始运行所有测试...\n")
    
    tests = [
        test_health,
        test_models,
        test_version,
        test_generate,
        test_chat,
        test_openai_chat
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n==============================")
    print(f"测试完成: {passed}/{total} 测试通过")
    print("==============================")
    
    if passed == total:
        print("🎉 所有测试通过！服务运行正常")
    else:
        print("⚠️  部分测试失败，请检查服务配置")

if __name__ == "__main__":
    run_tests()