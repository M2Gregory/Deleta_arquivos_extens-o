import os
import PySimpleGUI as sg
import datetime

# Função para percorrer os diretórios recursivamente e deletar os arquivos
def deletar_arquivos_recursivamente(diretorio, extensoes, arquivos_deletados):
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        if os.path.isdir(caminho_arquivo):
            # Se for uma subpasta, chama a função recursivamente para percorrê-la
            deletar_arquivos_recursivamente(caminho_arquivo, extensoes, arquivos_deletados)
        elif nome_arquivo.endswith(tuple(extensoes)):
            # Se o arquivo corresponder às extensões fornecidas, deleta-o
            os.remove(caminho_arquivo)
            arquivos_deletados.append(caminho_arquivo)


# Função para deletar arquivos com base no caminho e extensão
def deletar_arquivos(caminho, extensoes):
    try:
        arquivos_deletados = []
        deletar_arquivos_recursivamente(caminho, extensoes, arquivos_deletados)

        if arquivos_deletados:
            resultado_str = "Arquivos deletados:\n" + "\n".join(arquivos_deletados)
            window["-OUTPUT-"].update(resultado_str)

            # Gerar o log com os arquivos deletados
            log_file = f"Log_Deleção{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.txt"
            with open(log_file, "w") as log:
                log.write("Arquivos deletados:\n")
                for arquivo_deletado in arquivos_deletados:
                    log.write(arquivo_deletado + "\n")

            sg.popup("Log gerado com sucesso!", title="Gerador de Log", non_blocking=True)

        else:
            resultado_str = f"Nenhum arquivo com a extensão '{', '.join(extensoes)}' foi encontrado em '{caminho}'."
            window["-OUTPUT-"].update(resultado_str)

    except Exception as e:
        resultado_str = f"Erro ao deletar os arquivos: {e}"
        window["-OUTPUT-"].update(resultado_str)


# Interface gráfica usando PySimpleGUI
if __name__ == "__main__":
    sg.theme("DarkGrey13")

    layout = [
        [sg.Button("Selecionar Diretório", size=(18, 1), button_color=("white", "#202020"), font=("bold", 14))],
        [sg.InputText(key="-CAMINHO-", size=(70, 1), background_color="#252526", text_color="white", border_width=1,
                      tooltip=('''- Use o botão para escolher o diretório.
- Pode digitar o caminho ou colar usando o 'Ctrl+v'.'''))],
        [sg.Text("Digite a extensão do arquivo:", font=("bold", 15), text_color="white")],
        [sg.InputText(key="-EXTENSAO-", size=(30, 1), background_color="#252526", text_color="white", border_width=1,
                      tooltip=('''- Insira o ponto juntamente com a extensão. (Exemplo:.txt).
- Ao adicionar duas ou mais extensões, separe usando a vírgula.'''))],
        [sg.Button("Deletar Arquivos", size=(18, 1), button_color=("white", "#202020"), font=("bold", 14))],
        [sg.Output(size=(80, 10), background_color="#252526", text_color="white", font=("Courier New", 10),
                   key="-OUTPUT-")]
    ]

    window = sg.Window("Deleta Arquivos", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Selecionar Diretório":
            caminho = sg.popup_get_folder("Selecione o diretório", no_window=True, keep_on_top=True)
            if caminho:
                window["-CAMINHO-"].update(caminho)
        elif event == "Deletar Arquivos":
            caminho = values["-CAMINHO-"]
            extensoes = values["-EXTENSAO-"].replace(",", " ").split()
            deletar_arquivos(caminho, extensoes)

    window.close()
