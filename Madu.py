from youtube_transcript_api import YouTubeTranscriptApi
import anthropic
client = anthropic.Anthropic()

def pegar_id_do_video(url):
    if "youtu.be" in url:
        id_video =  url.split("/")[-1]
        return id_video
    elif "v=" in url:
        id_video = url.split("v=")[1].split("&")[0]
         
    return id_video


def pegar_transcricao(video_id):
    transcricao = YouTubeTranscriptApi.get_transcript(video_id)
    
    texto_completo = ""
    for pedaco in transcricao:
        texto_completo += pedaco["text"] + " "
    
    return texto_completo


def resumir_texto(texto):
    mensagem = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
         messages=[
        {"role": "user", "content": f"Resuma esse texto {texto}"}
    ]
    )
    
    return mensagem.content[0].text

def main():
    url = input("Cole o link do vídeo: ")
    video_id = pegar_id_do_video(url)
    transcricao = pegar_transcricao(video_id)
    resumo = resumir_texto(transcricao)
    print(resumo)

if __name__ == "__main__":
    main()  