#    Copyright (c) 2021 Danish_00
#    Improved By @Zylern


from decouple import config
import os
import subprocess
import telebot

# Read configuration variables from the environment or a .env file
APP_ID = config("APP_ID", cast=int)
API_HASH = config("API_HASH")
BOT_TOKEN = config("BOT_TOKEN")
DEV = 1664850827
OWNER = config("OWNER")
ffmpegcode = ["-preset faster -c:v libx265 -s 854x480 -x265-params 'bframes=8:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1' -metadata 'title=Encoded By TGVid-Comp (https://github.com/Zylern/TGVid-Comp)' -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 1"]
THUMBNAIL = config("THUMBNAIL", default="https://telegra.ph/file/f9e5d783542906418412d.jpg")

# Initialize your Telegram bot token
bot = telebot.TeleBot(BOT_TOKEN)

# Specify the directory to monitor for new video files
directory_to_monitor = 'path/to/directory'

@bot.message_handler(commands=['compress'])
def handle_compress_video(message):
    # Extract the parameters from the Telegram command
    command_parts = message.text.split(' ')
    if len(command_parts) != 4:
        bot.reply_to(message, 'Invalid command! Usage: /compress input_file output_file crf preset')
        return

    input_file = command_parts[1]
    output_file = command_parts[2]
    crf = command_parts[3]
    preset = command_parts[4]

    try:
        # Set the FFmpeg command with the specified options
        command = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', 'libx264',
            '-crf', str(crf),
            '-preset', preset,
            '-c:a', 'aac',
            '-b:a', '128k',
            output_file
        ]

        # Execute the FFmpeg command
        subprocess.run(command)

        bot.reply_to(message, 'Video compression completed successfully!')
    except Exception as e:
        bot.reply_to(message, f'An error occurred during video compression: {str(e)}')

def compress_new_videos():
    for filename in os.listdir(directory_to_monitor):
        if filename.endswith('.mp4'):
            input_file = os.path.join(directory_to_monitor, filename)
            output_file = os.path.join(directory_to_monitor, 'compressed_' + filename)

            try:
                # Set the FFmpeg command with default compression options
                command = [
                    'ffmpeg',
                    '-i', input_file,
                    '-c:v', 'libx264',
                    '-crf', '23',
                    '-preset', 'medium',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    output_file
                ]

                # Execute the FFmpeg command
                subprocess.run(command)
                
                print(f'Video {filename} compressed successfully!')
            except Exception as e:
                print(f'An error occurred during compression of {filename}: {str(e)}')

# Uncomment the following line to enable automatic video compression
# compress_new_videos()

# Start the Telegram bot
bot.polling()

