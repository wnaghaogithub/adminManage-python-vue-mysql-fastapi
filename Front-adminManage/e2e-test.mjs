import puppeteer from 'puppeteer-core'

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
const BASE = 'http://127.0.0.1:5173'
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

const pageErrors = []
const consoleErrors = []
const result = {}

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  args: ['--no-sandbox', '--disable-gpu', '--window-size=1400,900'],
})

try {
  const page = await browser.newPage()
  await page.setViewport({ width: 1400, height: 900 })

  page.on('pageerror', (e) => pageErrors.push(e.message))
  page.on('console', (m) => {
    if (m.type() === 'error') consoleErrors.push(m.text())
  })

  // 1. 登录
  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle0', timeout: 30000 })
  await page.waitForSelector('.login-btn', { timeout: 10000 })
  await page.click('.login-btn')
  await page.waitForSelector('.sidebar-menu', { timeout: 10000 })
  result.loginOk = true

  // 2. 切换到「文章列表」
  await page.evaluate(() => {
    const item = [...document.querySelectorAll('.el-menu-item')].find((i) =>
      i.textContent.includes('文章列表')
    )
    item && item.click()
  })
  await sleep(1200)
  result.articlePageOk = !!(await page.$('.search-box'))
  result.title = await page.title()

  // 3. 打开新增弹窗
  await page.evaluate(() => {
    const btn = [...document.querySelectorAll('button')].find((b) =>
      b.textContent.includes('新增文章')
    )
    btn && btn.click()
  })
  await page.waitForSelector('.el-dialog', { timeout: 8000 })
  result.dialogOpened = true

  // 4. 等待 wangEditor 初始化
  await sleep(1500)
  result.editorContentEditable = !!(await page.$('[contenteditable="true"]'))
  result.toolbarBtnCount = await page.evaluate(
    () => document.querySelectorAll('.w-e-bar-item').length
  )

  // 5. 填标题
  await page.type('input[placeholder="请输入文章标题"]', '端到端测试文章')
  await sleep(200)

  // 6. 选类型「编程」
  await page.evaluate(() => {
    const sel = [...document.querySelectorAll('.el-dialog .el-select')].find((s) =>
      s.textContent.includes('请选择文章类型')
    )
    const trigger = sel && (sel.querySelector('.el-select__wrapper') || sel)
    trigger && trigger.click()
  })
  await sleep(600)
  await page.evaluate(() => {
    const opt = [...document.querySelectorAll('.el-select-dropdown__item')].find(
      (o) => o.textContent.trim() === '编程'
    )
    opt && opt.click()
  })
  await sleep(300)
  result.typeSelected = await page.evaluate(() =>
    [...document.querySelectorAll('.el-dialog .el-select')].some((s) =>
      s.textContent.includes('编程')
    )
  )

  // 7. 输入富文本内容
  await page.click('[contenteditable="true"]')
  await page.type('[contenteditable="true"]', '这是端到端测试的正文内容。')
  await sleep(300)

  // 8. 提交（弹窗 footer 的「新 增」）
  await page.evaluate(() => {
    const btn = [...document.querySelectorAll('.el-dialog__footer button')].find(
      (b) => b.textContent.includes('新') && b.textContent.includes('增')
    )
    btn && btn.click()
  })
  await sleep(1500)
  result.createListHasItem = await page.evaluate(() =>
    document.body.textContent.includes('端到端测试文章')
  )

  // 9. 编辑回填验证
  await page.evaluate(() => {
    const row = [...document.querySelectorAll('.el-table__body tr')].find((tr) =>
      tr.textContent.includes('端到端测试文章')
    )
    const edit = row && [...row.querySelectorAll('button')].find((b) => b.textContent.includes('编辑'))
    edit && edit.click()
  })
  await sleep(1200)
  result.editTitleBackfill = await page.evaluate(() => {
    const inp = document.querySelector('input[placeholder="请输入文章标题"]')
    return inp ? inp.value : null
  })
  result.editEditorHasContent = await page.evaluate(() => {
    const el = document.querySelector('[contenteditable="true"]')
    return el ? el.textContent.includes('端到端测试') : false
  })

  // 10. 关闭编辑弹窗
  await page.evaluate(() => {
    const btn = [...document.querySelectorAll('.el-dialog__footer button')].find((b) =>
      b.textContent.includes('取')
    )
    btn && btn.click()
  })
  await sleep(800)

  // 11. 删除验证
  await page.evaluate(() => {
    const row = [...document.querySelectorAll('.el-table__body tr')].find((tr) =>
      tr.textContent.includes('端到端测试文章')
    )
    const del = row && [...row.querySelectorAll('button')].find((b) => b.textContent.includes('删除'))
    del && del.click()
  })
  await sleep(800)
  await page.evaluate(() => {
    const btn = [...document.querySelectorAll('.el-message-box button')].find((b) =>
      b.textContent.includes('确')
    )
    btn && btn.click()
  })
  await sleep(1500)
  result.deleteOk = !(await page.evaluate(() =>
    document.body.textContent.includes('端到端测试文章')
  ))

  await browser.close()
} catch (err) {
  result.fatal = err.message
  try {
    await browser.close()
  } catch {}
}

result.pageErrors = pageErrors
result.consoleErrors = consoleErrors
console.log(JSON.stringify(result, null, 2))
