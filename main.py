from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import numpy as np
from genetic_algorithm import Cidade, AlgoritmoGenetico, TAMANHO_POPULACAO, TAXA_MUTACAO, GERACOES, TAMANHO_TORNEIO, TAMANHO_GRID, MAX_COMPRIMENTO_CAMINHO

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, tuple):
            return list(obj)
        return super().default(obj)

app = FastAPI()

# Monta arquivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/api/nova-cidade")
async def nova_cidade():
    cidade = Cidade.gerar()
    return cidade.para_dicionario()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@app.websocket("/ws/otimizar")
async def otimizar(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        # Obtém dados da cidade inicial
        data = await websocket.receive_text()
        cidade_data = json.loads(data)
        
        # Converte listas em tuplas para pontos
        cidade_data['ponto_inicio'] = tuple(cidade_data['ponto_inicio'])
        cidade_data['ponto_fim'] = tuple(cidade_data['ponto_fim'])
        cidade_data['pontos_inundacao'] = [tuple(p) for p in cidade_data['pontos_inundacao']]
        
        # Cria instancias da cidade e do algoritmo genetico
        cidade = Cidade(
            grid=np.array(cidade_data['grid']),
            pontos_inundacao=cidade_data['pontos_inundacao'],
            ponto_inicio=cidade_data['ponto_inicio'],
            ponto_fim=cidade_data['ponto_fim']
        )
        ga = AlgoritmoGenetico(cidade)
        
        # Executa otimizacao e envia atualizacoes
        while True:
            estado = ga.evoluir()
            # Converte estado para formato serializavel JSON
            json_estado = json.dumps(estado, cls=NumpyEncoder)
            await websocket.send_text(json_estado)
            
            if estado['completo']:
                break
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Erro WebSocket: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        manager.disconnect(websocket)
        await websocket.close()

@app.get("/api/parametros")
async def get_parametros():
    return {
        "tamanho_populacao": TAMANHO_POPULACAO,
        "taxa_mutacao": TAXA_MUTACAO,
        "geracoes": GERACOES,
        "tamanho_torneio": TAMANHO_TORNEIO,
        "tamanho_grid": TAMANHO_GRID,
        "max_comprimento_caminho": MAX_COMPRIMENTO_CAMINHO
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)