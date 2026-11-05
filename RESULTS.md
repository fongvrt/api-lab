# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18 ชื่อ (นับจาก list `names` ใน JSON response ของ `GET /api/names` ด้วย `len()` ใน Python)
- Step 0.3, status code of the request without a token: 401 พร้อม body `{"error":"authentication failed"}` (เมื่อส่งพร้อม header จาก `auth.txt` ได้ 200 และ `{"tools":["Knife","Pizza cutter","Scissors"]}`)
- Step 0.4, the name of your pizza: The High Bolognese (ได้จาก `POST /api/pizza` พร้อม `veg.json`, ingredient ทั้ง 6 อย่างเป็น `"vegetarian":true` และ tool ที่ใช้ตัดคือ Scissors)
- Step 0.12, results of the three runs without a session (optional): ครั้งที่ 1 passed, ครั้งที่ 2 failed, ครั้งที่ 3 failed (passed 1 จาก 3 ครั้ง) ทุกครั้งสร้าง user ได้ 201 แต่ใน 2 ครั้งที่ fail การ login ได้ `401` แทน `200` (`assert 401 == 200`) เพราะไม่มี cookie AWSALB load balancer จึงส่ง login ไปยัง server ที่ไม่รู้จัก user ใหม่ ผลแบบนี้คือ flaky test
- Step 0.16, blocks of "how many of the three tools are excluded": 4 block ที่ไม่ทับกันและครอบคลุมทุกค่า (0 ถึง 3 tool)
  - 0 tool: `[]` → 200 ✔
  - 1 tool: `["Knife"]`, `["Scissors"]` (2 input เดิมของใบงาน) → 200 ✔
  - 2 tool: `["Knife", "Pizza cutter"]` → 200 ✔
  - 3 tool (exclude ครบทุก tool): `["Knife", "Pizza cutter", "Scissors"]` → **500 พร้อม body ว่าง** ✘ block นี้ทำให้เจอ Defect 1

## Defect report
- Title: Defect 1: `POST /api/pizza` ที่ exclude ครบทั้ง 3 tool ได้ 500 พร้อม body ว่าง แทนที่จะได้ 400 พร้อม JSON error message
- Request:
  - Method: `POST`
  - URL: `https://quickpizza.grafana.com/api/pizza`
  - Header: `Authorization: token abcdef0123456789` (จาก `auth.txt`)
  - Body: `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}` (จาก `all_tools.json`)
  - คำสั่ง: `curl -i -H "@auth.txt" -d "@all_tools.json" https://quickpizza.grafana.com/api/pizza`
- Expected result: product owner กำหนดว่า request ที่ไม่มีพิซซ่าใดตอบได้ต้องได้ status `400` พร้อม JSON error message (เช่น `{"error": "..."}`) และห้ามได้ `500`
- Actual result: status `HTTP/2 500`, `content-length: 0` (body ว่าง ไม่มี `content-type`) ได้ผลเดียวกันทั้งใน pytest (`test_all_tools_excluded_is_refused`, `assert 500 == 200` ก่อนย้ายเป็น xfail) และใน curl เมื่อ 2026-11-05
- Severity: Medium เพราะลูกค้าที่ exclude ครบทุก tool จะไม่ได้รับพิซซ่าอยู่แล้ว ระบบจึงไม่ได้เสียหายหรือข้อมูลรั่ว แต่ app ที่เรียก API จะได้ 500 ที่ไม่มีข้อความ ทำให้บอกผู้ใช้ไม่ได้ว่าผิดตรงไหน แยกไม่ออกจาก server ล่มจริง และอาจ retry ซ้ำโดยไม่จำเป็น

## Part A
- Step A4, status codes when the other user reads, changes and deletes:

## Part B
1.
2.
3.
4.
5.
6.
7.
8.
