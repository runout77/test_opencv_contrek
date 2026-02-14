import cv2
import numpy as np
import time
import os
import sys
from datetime import datetime, timezone

DRAW = "--draw" in sys.argv

images = [
  {'image': 'test_1024x1024', 'w': 1024, 'h': 1024},
  {'image': 'test_4096x4096', 'w': 4096, 'h': 4096},
  {'image': 'test_10000x10000', 'w': 10000, 'h': 10000},
  {'image': 'test_10240x10240', 'w': 10240, 'h': 10240},
  {'image': 'test_10240x10240_2', 'w': 10240, 'h': 10240},
  {'image': 'test_15360x15360', 'w': 15360, 'h': 15360},
  {'image': 'test_20480x20480', 'w': 20480, 'h': 20480},
]
for image in images:
  image_path = f"images/{image['image']}.png" 
  print(f"Processing {image_path} ....")
  start = time.time()
  img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  t_img = time.time()

  if img is None:
    print("Error: Image not found.")
    exit()

  channels = img.shape[2] if len(img.shape) > 2 else 1
  if channels == 4:
    exclude_color = np.array([255, 255, 255, 255], dtype=np.uint8)
  else:
    exclude_color = np.array([255, 255, 255], dtype=np.uint8)

  mask = cv2.inRange(img, exclude_color, exclude_color)
  mask = cv2.bitwise_not(mask) 
  contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

  external_count = 0
  internal_count = 0
  if hierarchy is not None:
    for i in range(len(contours)):
      parent = hierarchy[0][i][3]
      if parent == -1:
        external_count += 1
      else:
        internal_count += 1
  image['inner'] = internal_count
  image['outer'] = external_count

  t_proc = time.time()
  image['time'] = t_proc - start

  if DRAW:
    result = np.full(img.shape[:2] + (3,), 255, dtype=np.uint8)
    if hierarchy is not None:
      h_data = hierarchy[0]
      num_contours = len(contours)
      levels = np.zeros(num_contours, dtype=int)
      for i in range(num_contours):
          parent = h_data[i][3]
          if parent != -1:
              levels[i] = levels[parent] + 1
      pari = [contours[i] for i in range(num_contours) if levels[i] % 2 == 0]
      dispari = [contours[i] for i in range(num_contours) if levels[i] % 2 != 0]

      if pari:
          cv2.drawContours(result, pari, -1, (0, 0, 255), 1)  
      if dispari:
          cv2.drawContours(result, dispari, -1, (0, 128, 0), 1)
    end = time.time()
    cv2.imwrite(f"output/{image['image']}_opencv.png", result)



import os
import datetime
from bs4 import BeautifulSoup

file_path = "report.html"
original_template = "report_ori.html"
now_utc = datetime.datetime.now(datetime.timezone.utc)
display_time = now_utc.strftime("%Y-%m-%d %H:%M")
if os.path.exists(file_path):
    source_to_read = file_path
    print(f"Updating existing report: {file_path}")
elif os.path.exists(original_template):
    source_to_read = original_template
    print(f"Report not found. Using default template: {original_template}")
else:
    print(f"Errore: Nor {file_path} or {original_template} found!")
    exit()
with open(source_to_read, 'r', encoding='utf-8') as f:
    doc = BeautifulSoup(f, 'lxml')
tbody = doc.select_one('#report-body')
if tbody:
    rows = doc.select('tr[count]')
    counts = [int(r['count']) for r in rows if r.has_attr('count')]
    current_count = max(counts) if counts else 0
    for entry in images:
        image_id = entry['image']
        target_cell = doc.select_one(f"tr[count='{current_count}'] td[type='python'].pending.{image_id}")
        target_row_count = current_count
        if target_cell is None:
            target_row_count = current_count + 1
            new_row_html = f"""
            <tr count="{target_row_count}">
                <td>{target_row_count}</td>
                <td>{display_time}</td>
                <td>{image_id}</td>
                <td>{entry['w']}x{entry['h']}</td>
                <td type="python" class="pending {image_id}">Pending...</td>
                <td type="ruby" class="pending {image_id}">Pending...</td>
            </tr>
            """
            new_row = BeautifulSoup(new_row_html, 'html.parser').tr
            tbody.insert(0, new_row)          
        python_cell = doc.select_one(f"tr[count='{target_row_count}'] td[type='python'].pending.{image_id}")     
        if python_cell:
            formatted_time = f"{entry['time']:.6f} s"
            python_content = f"{formatted_time} (polylines outer={entry['outer']}, inner={entry['inner']})"          
            python_cell.string = python_content
            python_cell['class'] = [image_id]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(doc))
