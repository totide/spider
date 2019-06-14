# spider

简单验证码识别: tesseract-ocr、 pytesseract

滑动验证码破解思路:
  1. 获得没有缺口的验证码图片
  2. 获得有缺口的验证码图片
  3. 对比两张图片所有RGB像素点，得到不一样的像素点的x值,即要移动的距离
  4. 利用selenium模拟人的行为习惯(先匀加速后匀减速拖动)，把需要拖动的总距离分成一段一段小的轨迹
  5. 按照轨迹拖动，完成验证
  
解析html方式:
  1. xpath; 例如第三方库lxml(C语言编写的)
  2. BeatifulSoup;
  3. 正则表达式
  4. css选择器

爬虫框架: scrapy

模拟浏览器行为:
  selenium + 浏览器驱动(Chrome、FireFox等)
  
