const setRootFontSize = () => {
  // 获取窗口宽度
  const width = window.innerWidth

  // 设置基准值，例如：设计稿宽度为 375px
  const baseWidth = 1920

  // 计算根字体大小
  const rootValue = (width / baseWidth) * 16 // 假设 1rem = 16px

  // 设置根元素的字体大小
  document.documentElement.style.fontSize = `${rootValue}px`
}

// 初始调用
setRootFontSize()

// 监听窗口大小变化
window.addEventListener('resize', setRootFontSize)
