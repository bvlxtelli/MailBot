from my_lib import *
from mailbot import *

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

from bots import *

if dia_da_semana in ['Segunda', 'Quarta', 'Sexta']:
    
    enviar_maiores_quebras()

if dia_da_semana in ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']:
    
    enviar_sacolas()
    enviar_bolos()
    enviar_qbc_troca_665()

    enviar_saldo_maior_que_ep()
    enviar_duplicidades_gerenciais()

    enviar_quebra_campanha()
    enviar_divergencias_altas()

if dia_da_semana == 'Segunda':
    
    enviar_vencidos()
    enviar_sem_venda()

if dia_da_semana == 'Quarta':
    
    enviar_agendas()
    enviar_agendas_por_valor()

if dia_da_semana == 'Quinta':
    
    enviar_suspeitos_pendentes()

if dia_da_semana == 'Sexta':
    
    enviar_pereciveis()



