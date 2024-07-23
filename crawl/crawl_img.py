import requests
import os

start_at = int(input('bat dau tu: '))
end_at = int(input('ket thuc tai: '))
choose = input('which to crawl: nam/nu/couple (0/1/2)')

if(choose == '1'):
    url_end = '_nu.jpg'
elif(choose == '0'):
    url_end = "_nam.jpg"
elif(choose == '2'):
    url_end = "_audio_images.jpg"

success = 0

for i in range(start_at, end_at):
    url = f"https://love.nerman.com.vn/storage/audio/{i}/{i}" + url_end
    
    response = requests.get(url)
    if (response.status_code == 200):
        save_directory = f"C:/Users/PC/Desktop/cal/cal_repo/crawl_data/img/{i}"
        os.makedirs(save_directory, exist_ok=True)
        
        file_path = os.path.join(save_directory, f'{i}{url_end}')
        with open(file_path, 'wb') as file:
            file.write(response.content)
        success +=1
        print(f'{i}: done')
    
print(f'done: {success}/{end_at-start_at+1}')
            
