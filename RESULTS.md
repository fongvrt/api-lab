# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18 ชื่อ (นับจาก list `names` ใน JSON response ของ `GET /api/names` ด้วย `len()` ใน Python)
- Step 0.3, status code of the request without a token: 401 พร้อม body `{"error":"authentication failed"}` (เมื่อส่งพร้อม header จาก `auth.txt` ได้ 200 และ `{"tools":["Knife","Pizza cutter","Scissors"]}`)
- Step 0.4, the name of your pizza: The High Bolognese (ได้จาก `POST /api/pizza` พร้อม `veg.json`, ingredient ทั้ง 6 อย่างเป็น `"vegetarian":true` และ tool ที่ใช้ตัดคือ Scissors)
- Step 0.12, results of the three runs without a session (optional): ครั้งที่ 1 passed, ครั้งที่ 2 failed, ครั้งที่ 3 failed (passed 1 จาก 3 ครั้ง) ทุกครั้งสร้าง user ได้ 201 แต่ใน 2 ครั้งที่ fail การ login ได้ `401` แทน `200` (`assert 401 == 200`) เพราะไม่มี cookie AWSALB load balancer จึงส่ง login ไปยัง server ที่ไม่รู้จัก user ใหม่ ผลแบบนี้คือ flaky test
- Step 0.16, blocks of "how many of the three tools are excluded":

## Defect report
- Title:
- Request:
- Expected result:
- Actual result:
- Severity:

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
