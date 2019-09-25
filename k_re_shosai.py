import pandas as pd

df = pd.read_csv('kanazawa_0.csv')
point = [i.replace("['", '').replace("']", '').split() for i in list(df['詳細'])]


def check_empty(data):
    if data == '':
        g = '-'
    else:
        g = data
    return g


export_data = []
for i in point:
    del i[0]
    print('iの中身', len(i))
    shozaiti = check_empty(i[0].replace('所在地', ''))
    kotu = check_empty(i[1].replace('交通', ''))
    toti_memseki = check_empty(i[2].replace('土地面積', ''))
    sido_futan_memseki = check_empty(i[3].replace('私道負担面積', ''))
    set_back = check_empty(i[4].replace('セットバック', ''))
    tatemono_menseki = check_empty(i[5].replace('建物面積', ''))
    tatemono_kozo = check_empty(i[6].replace('建物構造', ''))
    yoto_tiiki = check_empty(i[7].replace('用途地域', ''))
    tiku_nengetu = check_empty(i[8].replace('築年月', ''))
    kenpeiritu = check_empty(i[9].replace('建ぺい率', ''))
    yosekiritu = check_empty(i[10].replace('容積率', ''))
    totikenri = check_empty(i[11].replace('土地権利', ''))
    omonasetudo = check_empty(i[12].replace('主な接道', ''))
    madori = check_empty(i[13].replace('間取り', ''))
    setubi = check_empty(i[14].replace('設備', ''))
    if len(i) == 20:
        sonota_setubi = check_empty(i[15].replace('その他設備', ''))
        genkyo = check_empty(i[16].replace('現況', ''))
        hikiwatasijiki = check_empty(i[17].replace('引渡時期', ''))
        hikiwatasi_joken = check_empty(i[18].replace('引渡条件', ''))
        torihiki_taiyo = check_empty(i[19].replace('取引態様', ''))
    elif len(i) > 18:
        sonota_setubi = check_empty(i[15].replace('その他設備', ''))
        genkyo = check_empty(i[16].replace('現況', ''))
        hikiwatasijiki = check_empty(i[17].replace('引渡時期', ''))
        hikiwatasi_joken = '-'
        torihiki_taiyo = check_empty(i[18].replace('取引態様', ''))
    else:
        sonota_setubi = '-'
        genkyo = check_empty(i[15].replace('現況', ''))
        hikiwatasijiki = check_empty(i[16].replace('引渡時期', ''))
        hikiwatasi_joken = '-'
        torihiki_taiyo = check_empty(i[17].replace('取引態様', ''))
    data = [shozaiti, kotu, toti_memseki, sido_futan_memseki,
                        set_back, tatemono_menseki, tatemono_kozo,yoto_tiiki,
                        tiku_nengetu, kenpeiritu, yosekiritu, totikenri, omonasetudo, madori,
                        setubi, sonota_setubi, genkyo, hikiwatasijiki, hikiwatasi_joken,torihiki_taiyo
                        ]
    print('dataの中身は', len(data))
    export_data.append(data)
    # print(export_data)

data = pd.DataFrame(export_data)
data.to_csv(
    'remake_shosai.csv',
    # header=['所在地',
    #         '交通',
    #         '土地面積',
    #         '私道負担面積',
    #         'セットバック',
    #         '建物面積',
    #         '建物構造'
    #         '用途地域'
    #         '築年月'
    #         '建ぺい率'
    #         '容積率'
    #         '土地権利'
    #         '主な接道'
    #         '間取り'
    #         '設備'
    #         'その他設備'
    #         '現況'
    #         '引渡時期'
    #         '引渡条件'
    #         '取引態様'
    #         ],
    index=False,
    mode='a'
            )

