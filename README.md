# DALL-E 图像生成应用

## 介绍
DALL-E 图像生成应用是一个使用 Tkinter 库构建的 Python 应用程序，允许用户使用 OpenAI DALL-E 模型生成图像。该应用提供了一个用户友好的界面，用于与 DALL-E API 进行交互，从而基于用户提示创建独特和多样化的图像。

## 特性
- **模型选择：** 在不同的 DALL-E 模型之间进行选择，例如 "dall-e-2" 和 "dall-e-3"。
- **提示输入：** 在提供的文本输入中输入提示，以引导图像生成过程。
- **图像参数：** 调整各种参数，包括大小、生成图像数量、质量和风格。
- **API 密钥配置：** 输入 OpenAI API 密钥进行身份验证并访问 DALL-E API。
- **代理配置：** 可选设置 API 请求的代理。
- **图像导航：** 使用上一个和下一个按钮轻松导航生成的图像。
- **图像显示：** 在应用程序中查看生成的图像。
- **配置保存：** 自动保存和加载配置设置。
![屏幕截图 2024-01-10 153223](https://github.com/buwanyuanshen/DALLE-python/assets/144007759/00672c75-a7fe-4dac-b4db-906c3df01584)
![屏幕截图 2024-01-10 153051](https://github.com/buwanyuanshen/DALLE-python/assets/144007759/38e79f1a-acd0-4070-95f5-45a52f9611eb)
![屏幕截图 2024-01-10 162249](https://github.com/buwanyuanshen/DALLE-python/assets/144007759/9bf3724e-1297-45e8-8b47-d0fe3913cd85)
![(O4DSU$ MT}FU7OS~JX2R99](https://github.com/buwanyuanshen/DALLE-python/assets/144007759/c69e10f2-4932-4b1f-a760-7a67fa3991cf)

  

## 使用方法
1. **模型选择：**
   - 从下拉列表中选择 DALL-E 模型。

2. **提示输入：**
   - 在提供的文本输入中输入提示。

3. **图像参数：**
   - 设置所需的图像参数，如大小、生成图像数量、质量和风格。

4. **API 密钥配置：**
   - 输入由逗号分隔的 OpenAI API 密钥。

5. **代理配置：**
   - 可选地为 API 请求设置代理 URL。

6. **生成图像：**
   - 单击 "生成图片" 按钮以启动图像生成过程。

7. **浏览图像：**
   - 使用 "< 上一页" 和 "下一页 >" 按钮浏览生成的图像。

8. **图像显示：**
   - 在应用程序中查看生成的图像。

## 配置持久性
- **自动保存：** 在关闭应用程序时，配置设置会自动保存到 "dalle-config.json"。

## 依赖项
- Python 3.x
- Tkinter
- OpenAI==0.28.0
- PIL（Pillow）
- Requests

## 入门指南
1. 克隆存储库。
2. 使用 `pip install -r requirements.txt` 安装所需的依赖项。
3. 使用 `python Dalle Paint.py` 运行应用程序。

## 许可证
该项目根据 MIT 许可证进行许可 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。
