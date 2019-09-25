import pandas as pd

# df = pd.read_csv('kanazawa_0.csv')
# point = [i.replace("['", '').replace("']", '').split() for i in list(df['ポイント'])]
#
#
# def check_empty(data):
#     if data == '':
#         g = '-'
#     else:
#         g = data
#     return g
#
#
# export_data = []
# for i in point:
#     del i[0]
#     print(len(i))
#     print(i)
#     price = i[1]
#     madori = i[3]
#     shozaiti = i[5]
#     tatemono_menseki = i[7]
#     toti_menseki = i[9]
#     kozo_kaisu = i[11].replace('\\xa0', ' ').replace('交通', '')
#     if len(i) == 13:
#         kotu = i[12]
#         other = '-'
#     elif len(i) == 12:
#         kotu = i[11]
#         other = '-'
#     else:
#         kotu = i[13]
#         other = i[14:]
#     export_data.append([price, madori, shozaiti, tatemono_menseki, toti_menseki, kozo_kaisu, kotu, other])
#
# data = pd.DataFrame(export_data)
# data.to_csv(
#     'remake_pointo.csv',
#     # header=['価格',
#     #         '間取り',
#     #         '所在地',
#     #         '建物面積',
#     #         '土地面積',
#     #         '構造・階層',
#     #         '交通',
#     #         'その他'
#     #         ],
#     index=False,
#     mode='a'
#             )
#
df = pd.read_csv('karuizawa_fainally.csv')
print(df)