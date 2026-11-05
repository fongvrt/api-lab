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
- Step A4, status codes when the other user reads, changes and deletes: อ่าน (GET) = `404` `{"error":"not found"}`, แก้ (PUT) = `400` `{"error":"rating ID <id> not found"}`, ลบ (DELETE) = `400` `{"error":"rating ID <id> not found"}` ทั้ง 3 ครั้งอยู่ในช่วง 400–499 และเมื่อ owner อ่านกลับมา rating ไม่เปลี่ยน (3 ดาว, `pizza_id` เดิม)

## Part B
1. test ของเราคุยกับ server จริง จึงเจอ failure 2 แบบที่ unit test ที่ใช้ stub หาไม่เจอ (1) ปัญหาจาก infrastructure เช่น load balancer ที่ส่ง request ไปคนละ server จน login ได้ 401 (Step 0.12) (2) ปัญหาเมื่อส่วนต่าง ๆ ทำงานร่วมกัน เช่น 500 พร้อม body ว่างเมื่อ exclude ครบ 3 tool (Step 0.16) หรือ error message ที่มาจาก JSON decoder ของ Go โดยตรง ส่วนเหตุผลที่ควรเขียน unit test ด้วย คือ unit test เร็ว ให้ผลเหมือนเดิมทุกครั้ง ไม่ขึ้นกับเน็ตหรือ server ที่คนอื่นใช้ร่วมกัน และชี้ได้ตรงว่า function ไหนพัง
2. ข้อมูลที่สร้างด้วย public token เป็นของทุกคน คนอื่นอาจแก้หรือลบระหว่างที่ test เรารัน ทำให้ test fail แบบสุ่ม และเราเองก็อาจไปทำข้อมูลของคนอื่นพัง การสร้าง user ใหม่ชื่อไม่ซ้ำทุก test ทำให้แต่ละ test มีข้อมูลของตัวเองและเป็นอิสระต่อกัน ใน Project 2 จะใช้หลักเดียวกัน คือให้ fixture สร้างข้อมูลของกลุ่มเราเอง (เช่น ลูกค้า ตะกร้า หรือการจอง) ด้วยชื่อที่มี uuid ลบทิ้งหลัง test จบ และไม่แตะข้อมูลของกลุ่มอื่นเลย
3. QuickPizza มีหลาย server อยู่หลัง load balancer และแต่ละ server เก็บ user ของตัวเอง session จะเก็บ cookie AWSALB ไว้ request ถัดไปจึงไปถึง server ตัวเดิมที่รู้จัก user ที่เพิ่งสร้าง ใน Step 0.12 ที่ไม่ใช้ session ผล 3 ครั้งคือ passed, failed, failed ใน 2 ครั้งที่ fail สร้าง user ได้ 201 แต่ login ได้ 401 เพราะ request ไปตกที่ server ที่ไม่รู้จัก user นี้ แสดงว่า test แบบนี้เป็น flaky test
4. block ที่ทำให้เจอ defect คือ "exclude ครบทั้ง 3 tool" (`["Knife", "Pizza cutter", "Scissors"]`) 500 ที่ body ว่างแย่กว่า 400 ที่มีข้อความ เพราะ app ที่เรียก API แยกไม่ออกว่าเป็น input ผิดหรือ server ล่มจริง ไม่มีข้อความไปแสดงให้ผู้ใช้ และอาจ retry ซ้ำโดยเปล่าประโยชน์ ในขณะที่ 400 พร้อมข้อความบอกได้เลยว่าต้องแก้ input ตรงไหน test นี้เก็บไว้เป็น xfail แทนการลบ เพราะ defect ยังคงมองเห็นได้ใน report ทุกครั้งที่รัน โดย suite ส่วนที่เหลือยังผ่านทั้งหมด และ `strict=True` จะทำให้ run fail ทันทีที่ QuickPizza แก้ defect แล้ว เป็นสัญญาณให้เอา mark ออก ถ้าลบ test ทิ้งก็จะเสีย regression check ของจุดนี้ไป
5. base choice = 1 + Σ(จำนวน block − 1) = 1 + (3 − 1) + (4 − 1) + (2 − 1) + (3 − 1) = 1 + 2 + 3 + 1 + 2 = **9 test** (ตรงกับ 9 test ใน `test_create_rating.py`) ส่วน all combinations = 3 × 4 × 2 × 3 = **72 test**
6. ผลที่ได้จริงคือ อ่าน = `404`, แก้ = `400`, ลบ = `400` (`{"error":"rating ID <id> not found"}`) code ที่คาดไว้คือ `404 Not Found` ทั้ง 3 ครั้ง (สำหรับอีก user ถือว่า rating นี้ "ไม่มีอยู่" และไม่บอกด้วยว่ามีอยู่จริง) หรือ `403 Forbidden` ถ้าระบบยอมบอกว่ามี rating นี้แต่ไม่ใช่ของเรา ในด้าน security ไม่ใช่ defect เพราะทุกครั้งถูกปฏิเสธและข้อมูลไม่เปลี่ยน แต่ถือเป็น defect เล็กน้อยด้าน API contract เพราะ code ไม่สม่ำเสมอ และ `400 Bad Request` ผิดความหมาย เนื่องจาก request ไม่ได้ผิด format
7. `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` (GET อย่างเดียว) ได้ `HTTP/2 200` พร้อม `{"ratings":[...]}` 50 รายการที่เราไม่ได้สร้าง ทั้งที่ token `0000000000000000` เป็นค่าที่แต่งขึ้นเองและไม่ได้มาจากการ login ในขณะที่ `token short` ได้ 401 จึงดูเหมือน server ตรวจแค่ความยาวของ token (16 ตัวอักษร) ไม่ได้ตรวจว่าเป็น token ที่ออกให้จริง นี่เป็น defect ด้าน security ถ้าเป็นระบบจริง คนแปลกหน้าที่ไม่มีบัญชีจะอ่านข้อมูลได้โดยไม่ต้อง login และอาจสร้าง แก้ หรือลบข้อมูลในนามของ user คนอื่นได้ (เราไม่ได้ทดลองส่วนนี้ตามกฎของใบงาน)
8. สิ่งที่ API test ตรวจได้ดีกว่าคือ status code, error message และ validation ของ input แต่ละ field ได้ตรงและเร็ว รวมถึง request ที่หน้าเว็บไม่ยอมให้ส่ง เช่น stars = 3.5 หรือ token ปลอม ส่วนสิ่งที่ต้องทดสอบผ่านหน้าเว็บเท่านั้นคือสิ่งที่ผู้ใช้เห็นจริงบนหน้าจอ เช่น ข้อความ error แสดงถูกที่หรือไม่ layout เป็นอย่างไร และปุ่มกดใช้งานได้หรือไม่
