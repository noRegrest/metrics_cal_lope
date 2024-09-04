const https = require('https');
const fs = require('fs');
const path = require('path');
const { finished } = require('stream/promises');
require('dotenv').config();

async function downloadFile(fileUrl, downloadPath, contentType) {
    const options = {
        method: 'GET',
        headers: { 'Content-Type': contentType },
    };

    return new Promise((resolve, reject) => {
        const req = https.get(fileUrl, options, async (res) => {
            if (res.statusCode === 200) {
                const dir = path.dirname(downloadPath);
                await fs.promises.mkdir(dir, { recursive: true });

                const file = fs.createWriteStream(downloadPath);
                res.pipe(file);

                file.on('finish', async () => {
                    try {
                        await finished(file);
                        resolve();
                    } catch (err) {
                        console.error('Error finishing file:', err);
                        reject(err);
                    }
                });

                file.on('error', (err) => {
                    console.error('File error:', err);
                    file.close(() => {
                        fs.promises.unlink(downloadPath).catch(() => {});
                    });
                    reject(err);
                });
            } else {
                reject(new Error(`Failed to download ${fileUrl}. Status code: ${res.statusCode}`));
            }
        });

        req.on('error', (err) => {
            console.error(`Request error for ${fileUrl}:`, err);
            reject(err);
        });
    });
}

async function downloadAllFiles(s, e, batchSize, delayBetweenBatches) {
    const start = s;
    const end = e;
    const tasks = [];
    const totalBatches = Math.ceil(((end - start + 1) * 4) / batchSize);
    let completedBatches = 0;

    // Create tasks
    for (let i = start; i <= end; i++) {
        const fileUrlWav = `https://love.nerman.com.vn/storage/audio/${i}/${i}_audio.wav`;
        const fileUrlImgNam = `https://love.nerman.com.vn/storage/audio/${i}/${i}_nam.jpg`;
        const fileUrlImgNu = `https://love.nerman.com.vn/storage/audio/${i}/${i}_nu.jpg`;
        const fileUrlImgCouple = `https://love.nerman.com.vn/storage/audio/${i}/${i}_audio_images.jpg`;

        const downloadPathAudio = path.join(__dirname, '17K', 'audio', `${i}_audio.wav`);
        const downloadPathImageNam = path.join(__dirname, '17K', 'img', `${i}`, `${i}_nam.jpg`);
        const downloadPathImageNu = path.join(__dirname, '17K', 'img', `${i}`, `${i}_nu.jpg`);
        const downloadPathImageCouple = path.join(__dirname, '17K', 'img', `${i}`, `${i}_audio_images.jpg`);

        // const downloadPathImageCouple = path.join(__dirname, 'download_test', `${i}_audio_images.jpg`);

        tasks.push({
            url: fileUrlWav,
            path: downloadPathAudio,
            contentType: 'audio/wav',
        });
        tasks.push({
            url: fileUrlImgNam,
            path: downloadPathImageNam,
            contentType: 'image/jpeg',
        });
        tasks.push({
            url: fileUrlImgNu,
            path: downloadPathImageNu,
            contentType: 'image/jpeg',
        });
        tasks.push({
            url: fileUrlImgCouple,
            path: downloadPathImageCouple,
            contentType: 'image/jpeg',
        });
    }

    // Execute tasks in batches
    for (let i = 0; i < tasks.length; i += batchSize) {
        const batch = tasks.slice(i, i + batchSize);
        await Promise.all(
            batch.map(async (task) => {
                try {
                    await downloadFile(task.url, task.path, task.contentType);
                } catch (error) {}
            })
        );
        completedBatches++;
        const progress = Math.round((completedBatches / totalBatches) * 100);

        console.clear();
        console.log(`${progress}% completed.`);

        await new Promise((resolve) => setTimeout(resolve, delayBetweenBatches));
    }
}

const batchSize = parseInt(process.env.BATCH_SIZE);
const delayBetweenBatches = parseInt(process.env.DELAY_BETWEEN_BATCHES);
const startFrom = parseInt(process.env.START_FROM);
const endAt = parseInt(process.env.END_AT);

downloadAllFiles(startFrom, endAt, batchSize, delayBetweenBatches);
