from my_lib import *
from mailbot import *

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

from mailbot_agendas_semanais import enviar_agendas
from mailbot_agendas_semanais_vlr import enviar_agendas_por_valor
from mailbot_bolos import enviar_bolos
from mailbot_maiores_qbc_flv import enviar_maiores_quebras
from mailbot_pereciveis import enviar_pereciveis
from mailbot_sacolas import enviar_sacolas
from mailbot_sem_venda import enviar_sem_venda
from mailbot_suspeitos_pendentes import enviar_suspeitos_pendentes
from mailbot_vencidos import enviar_vencidos
from mailbot_qbc_troca_665 import enviar_qbc_troca_665
from mailbot_quebra_campanha import enviar_quebra_campanha
from mailbot_divergencias_altas import enviar_divergencias_altas

if dia_da_semana == 'Segunda':

    enviar_maiores_quebras()
    enviar_vencidos()

    enviar_sacolas()
    enviar_bolos()
    enviar_qbc_troca_665()

    enviar_quebra_campanha()
    enviar_sem_venda()
    enviar_divergencias_altas()

if dia_da_semana == 'Terça':

    enviar_sacolas()
    enviar_bolos()
    enviar_qbc_troca_665()

    enviar_quebra_campanha()
    enviar_divergencias_altas()

if dia_da_semana == 'Quarta':

    enviar_maiores_quebras()

    enviar_sacolas()
    enviar_bolos()
    enviar_qbc_troca_665()

    enviar_agendas()
    enviar_agendas_por_valor()

    enviar_quebra_campanha()
    enviar_divergencias_altas()

if dia_da_semana == 'Quinta':

    enviar_sacolas()
    enviar_bolos()
    enviar_qbc_troca_665()

    enviar_quebra_campanha()
    enviar_divergencias_altas()
    enviar_suspeitos_pendentes()
    

if dia_da_semana == 'Sexta':

    enviar_maiores_quebras()

    enviar_sacolas()
    enviar_bolos()
    enviar_qbc_troca_665()

    enviar_quebra_campanha()
    enviar_divergencias_altas()
    enviar_pereciveis()



