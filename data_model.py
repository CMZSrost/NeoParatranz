from dataclasses import dataclass


@dataclass
class attackmodes:
    """攻击类别"""

    id: int  # 代码标号
    strName: str  # 当前物品名称【需要翻译】
    strNotes: str  # 当前物品注释(一般留空,对游戏无影响)【需要翻译】
    nRange: int  # 攻击距离
    fDamageCut: float  # 切割伤害
    fDamageBlunt: float  # 钝器伤害
    strChargeProfiles: str  # 内容物/弹药的代码标号(结合chargeprofiles数据类别使用)
    nPenetration: int  # 穿透等级
    nType: int  # 攻击类别( 0 近战1 远程)
    strSnd: str  # 武器分类(注释:1 )
    bTransfer: bool  # 弹药位置转移(注释:2 )
    vAttackerConditions: str  # 攻击时的状态(结合conditions数据类别使用)
    strIMG: str  # 右下角武器图标
    fMorale: float  # 该武器默认为你带来的士气(注释:3 )
    strWieldPhrase: str  # 使用该武器进入战斗时的文字表达(注释:4 )【需要翻译】
    vAttackPhrases: str  # 使用该武器攻击敌人时的文字表达(注释:4 )【需要翻译】


@dataclass
class barterhexes:
    """交易区块"""

    id: int  # 代码标号
    nX: int  # X轴坐标
    nY: int  # Y轴坐标
    bBuys: bool  # 是否可以购买玩家的物品(0为不可以)
    nRestockTreasureID: int  # 引用的战利品数据(结合treasuretable数据类别使用)(注释1)


@dataclass
class battlemoves:
    """战斗动作"""

    id: int  # 代码标号
    strID: str  # 物品标号
    strName: str  # 动作名称【需要翻译】
    strNotes: str  # 动作注释(一般留空,对游戏无影响)【需要翻译】
    strSuccess: str  # 当该战斗动作执行成功后在游戏中显示的文本【需要翻译】
    strFail: str  # 当该战斗动作执行失败后在游戏中显示的文本【需要翻译】
    strPopUp: str  # 游戏内的动作说明【需要翻译】
    vChanceType: str  # 未知
    vUsConditions: str  # 该行动会为你带来的状态(结合conditions数据类别使用)
    vThemConditions: str  # 该行动会为敌方带来的状态
    vPairConditions: str  # 该行动对你带来的影响
    vUsFailConditions: str  # 当该行动失败时会对你带来的状态
    vThemFailConditions: str  # 当该行动失败时会对敌方带来的状态(注释1)
    vPairFailConditions: str  # 当该行动失败时会对你带来的影响
    vUsPreConditions: str  # 执行该行动的前置要求(注释2)
    nSeeThem: int  # 对方的暴露等级
    nSeeUs: int  # 自己的暴露等级
    bAllOutOfRange: bool  # 离开所有场上目标距离
    bInAttackRange: bool  # 攻击范围(注释3)
    nMinCharges: int  # 攻击次数(存疑)
    nMinRange: int  # 距离最小需求(注释4)
    nMaxRange: int  # 距离最大需求(注释4)
    nAttackModeType: int  # 攻击模式(注释5)
    vHexTypes: str  # (注释6)
    fChance: float  # 你可以使用该技能得的几率(按百分比算)
    fPriority: float  # 优先级(对玩家毫无用处,BOT专用)
    fDetect: float  # 执行该动作使你被发现的几率(如果你调整为0,那么你即使是在对方的脸上跳舞也不会被发现)
    fOrder: float  # 未知
    fFatigue: float  # 疲劳值
    bApproach: bool  # 该动作是否会使你接近对方
    bOffense: bool  # 是否是攻击性动作
    bFallBack: bool  # 该动作是否为远离动作
    bRetreat: bool  # 该动作是否为撤退动作
    bPosition: bool  # 该动作是否为姿势动作
    bPassive: bool  # 该动作是否为被动


@dataclass
class camptypes:
    """营地类型"""

    id: int  # 代码标号
    strDesc: str  # 该营地的描述【需要翻译】
    vImageList: str  # 该营地调用的图片
    aCapacities: str  # 营地大小
    nTreasureID: int  # 该营地的战利品池
    m_fAlertness: float  # 该营地的默认警戒值
    m_fVisibility: float  # 该营地的默认可见值
    WetTempAdjustMod: int  # 该营地的默认温度
    m_fHealPerHourMod: float  # 该营地默认每小时为你带来的恢复效果
    fSleepQuality: float  # 该营地默认为你带来的睡眠质量


@dataclass
class chargeprofiles:
    """内容物/弹药种类(结合攻击类别中的ChargeProfiles使用)"""

    nID: int  # 代码标号
    strName: str  # 物品名称【需要翻译】
    strItemID: str  # 物品ID
    fPerUse: float  # 每次使用所消耗的数量
    fPerHour: float  # 每小时所消耗数量(基本用于电器的电力消耗)
    fPerHourEquipped: float  # 装备在身上时每小时的消耗耐久(仅用于XM54过滤芯片)
    fPerHex: float  # 每移动一格所消耗的数量
    bDegrade: bool  # 是否会降解


@dataclass
class conditions:
    """状态"""

    id: int  # 代码标号
    strName: str  # 状态名称【需要翻译】
    strDesc: str  # 状态注释/描述【需要翻译】
    aFieldNames: str  # 该状态为你带来的效果(注释1)
    aModifiers: str  # 该状态为你带来的效果的具体影响数值
    aEffects: str  # 装甲效果
    bFatal: bool  # 是否为玩家带来死亡效果(得到这个状态你会不会暴毙)
    vIDNext: str  # 该状态下一阶段为你带来的新状态
    fDuration: float  # 持续时间
    bPermanent: bool  # 是否为会为你带来长期影响(如吃药、割伤等)
    vChanceNext: str  # 有多大几率该状态在下个阶段为你带来新的状态
    bStackable: bool  # 该状态是否可以堆叠
    bDisplay: bool  # 该状态是否可见
    bDisplayOther: bool  # 该状态是否可被其他人看见
    bDisplayGameOver: bool  # 该状态是否会在你的游戏总结中出现
    nColor: int  # 状态颜色(注释2)
    bResetTimer: bool  # 刷新时间/这里为一小时刷新(注释3)
    bRemoveAll: bool  # 未知
    bRemovePostCombat: bool  # 未知
    nTransferRange: int  # 传染距离(与技能距离不同的是,这里的-1为不传播)
    aThresholds: str  # 未知


@dataclass
class containertypes:
    """内容物属性与分类(结合物品类别中的nTreasureID与aContentIDs使用)"""

    id: int  # 代码标号
    strName: str  # 属性名称【需要翻译】


@dataclass
class creatures:
    """生物与生物派系"""

    id: int  # 代码标号
    strName: str  # 生物名称【需要翻译】
    strNamePublic: str  # 未接触时名称【需要翻译】
    strNotes: str  # 注释【需要翻译】
    strImg: str  # 该生物在地图上调用的图片
    vEncounterIDs: str  # 遇到该生物会触发的状态
    nMovesPerTurn: int  # 每回合的行动点数
    nTreasureID: int  # 战利品池(击杀掉落)
    nFaction: int  # 所属阵营
    vAttackModes: str  # 攻击方式(结合攻击类别使用)
    vBaseConditions: str  # 该生物生成时的基础状态
    nCorpseID: int  # 尸体编号(战利品池编号)
    vActivities: str  # 该生物的活动方式(注释1)


@dataclass
class creaturesources:
    """生物刷新点"""

    id: int  # 代码标号
    strName: str  # 生物名称【需要翻译】
    nX: int  # X轴坐标
    nY: int  # Y轴坐标
    nCreatureID: int  # 刷新的生物编号(结合生物与生物派系中的标号生成)
    nMin: int  # 最小刷新数量
    nMax: int  # 最大刷新数量(就是这个数据导致经常有一大群鹿刷在同一个区块)
    fWeight: float  # 重量(注释1)


@dataclass
class datafiles:
    """电子产品里的数据文本"""

    id: int  # 代码标号
    strName: str  # 数据名称【需要翻译】
    strDesc: str  # 数据详情【需要翻译】
    fValue: float  # 该资料值多少钱
    strImg: str  # 该数据所调用的图片


@dataclass
class dmcplaces:
    """底特律城区建筑"""

    id: int  # 代码标号
    strImg: str  # 建筑名称【需要翻译，但原先的汉化中没有汉化。也可以不汉化】
    nEncounterID: int  # 调用的剧情代码(结合encounters数据类别使用))
    nX: int  # X轴坐标
    nY: int  # Y轴坐标


@dataclass
class encounters:
    """剧情代码"""

    id: int  # 代码标号
    strName: str  # 该剧情的名称【需要翻译】
    strDesc: str  # 剧情文本【需要翻译】
    strImg: str  # 该剧情调用的图片
    nTreasureID: int  # 战利品池标号
    nRemoveTreasureID: int  # 移除的战利品池标号(注释1)
    aConditions: str  # 该剧情的附带状态(注释2)(结合conditions数据类别使用)
    aPreConditions: str  # 出现该剧情时必要的前置状态(注释3)
    fPrice: float  # 该剧情是否会让你的资产变动
    aResponses: str  # 玩家在经历该剧情时的回应(注释4)
    aMinimapHexes: str  # 小地图上显示的点(因为这个剧情是玩家主动触发,所以此数值为空)
    bRemoveCreatures: bool  # 该剧情发生时需要移除的生物(注释5)
    bRemoveUsed: bool  # 该剧情是否会移除你的物品
    nItemsID: int  # 发生该剧情时产生的物品
    nCreatureID: int  # 该剧情发生时需要增加的生物(注释同5)
    ptCreatureHex: str  # 该生物出现位置(注释同5)
    ptTeleport: str  # 发生该剧情时将玩家传送到该位置(0,0为不传送)
    ptEditor: str  # 未知
    nType: int  # 剧情类型(0为普通剧情,1为搜刮剧情)
    fLootChance: float  # 成功搜刮到物品的几率
    fAccidentChance: float  # 发生意外的几率(例如破楼倒塌)
    fCreatureChance: float  # 未知
    vAccidents: str  # 出现意外时发生的事件(注意:这个并不是调用conditions数据类别,而是调用相同的encounters)
    vLoot: str  # 但你搜刮成功时的战利品种类(结合conditions数据类别使用)


@dataclass
class encountertriggers:
    """事件触发器"""

    id: int  # 代码标号
    strName: str  # 触发的剧情名称【需要翻译】
    nEncounterID: int  # 触发器的代码标号
    fChance: float  # 触发几率
    bLocBased: bool  # 该触发器是否为固定位置触发
    bDateBased: bool  # 该触发器是否为固定时间触发
    bHexBased: bool  # 该触发器是否为固定场景触发
    bUnique: bool  # 该事件是否是独一无二的
    bAIPassable: bool  # 该事件是否能被AI触发
    aArea: str  # 该事件触发的位置
    dateMin: str  # 未知
    dateMax: str  # 未知
    aHexTypes: str  # 可触发该触发器的固定场景(结合hextypes数据类别使用)


@dataclass
class factions:
    """阵营/派系(与creatures数据息息相关)"""

    id: int  # 代码标号/阵营标号
    strName: str  # 阵营名称【需要翻译】
    dictFactions: str  # 与其他派系的声望


@dataclass
class forbiddenhexes:
    """保护区场景位置"""

    id: int  # 代码标号
    nX: int  # X轴坐标
    nY: int  # Y轴坐标
    strName: str  # 保护区所属阵营【需要翻译】


@dataclass
class gamevars:
    """游戏变量"""

    strName: str  # 变量名称
    strType: str  # 数值类型
    strValue: str  # 具体数值


@dataclass
class headlines:
    """头版头条(报纸)"""

    id: int  # 代码标号
    strHeadline: str  # 头版头条具体文本【需要翻译】


@dataclass
class hextypes:
    """地块类型"""

    id: int  # 代码标号
    strName: str  # 地块名称【需要翻译】
    strDesc: str  # 地块在游戏中显示的名称【需要翻译】
    nTerrainCost: int  # 在该地块上消耗的行动点数
    nVizLimiter: int  # 在该地块上减少的视距
    nVizIncrease: int  # 在该地块上增加的视距
    nTreasureID: int  # 在该地块上生成的战利品池
    bPassable: bool  # 可不可以移动到该地形
    nScavengeInitialID: int  # 当你初次搜刮该地形的时候所调用的战利品池
    nScavengeItemsIDPerHour: int  # 当你多次搜刮该地形的时候所调用的战利品池(注释1)
    nCampItems: int  # 营地类型
    vLightLevels: str  # 亮度等级(注释2)
    nDefaultCampID: int  # 默认营地的代码标号(结合treasuretable数据类别使用)
    nMinRange: int  # 如果玩家在此处遇到生物,那么玩家距离此生物的最小距离数
    nMaxRange: int  # 如果玩家在此处遇到生物,那么玩家距离此生物的最大距离数
    vCondIDs: str  # 进入该地块会为玩家带来的状态


@dataclass
class ingredients:
    """合成项"""

    nID: int  # 合成项目标号(注释1)
    strName: str  # 合成项名称【需要翻译】
    strRequiredProps: str  # ※※合成项属性※※(这条属性对于合成项极其重要)
    strForbidProps: str  # 合成项不可拥有的属性


@dataclass
class itemprops:
    """合成项属性/物品属性(以下称之为合成项属性)"""

    nID: int  # 合成项属性标号
    strPropertyName: str  # 合成项属性的名称(注释1)【需要翻译】


@dataclass
class itemtypes:
    """物品详情"""

    id: int  # 代码标号
    nGroupID: int  # 物品前ID
    nSubgroupID: int  # 物品后ID(注释1)
    strName: str  # 物品名称【需要翻译】
    strDesc: str  # 该物品在游戏中的名称【需要翻译】
    strDescAlt: str  # 真实描述(常用于需要技能识别的药品和弹药)【需要翻译】
    nCondID: int  # 真实描述的状态前置(比如此条目中的53对应的状态就是精通医学)
    vImageList: str  # 该物品调用的图片
    vSpriteList: str  # 在游戏大地图中显示的人物图片(注释2)
    vImageUsage: str  # 未知
    fWeight: float  # 该物品的重量
    fMonetaryValue: float  # 如果你狗屁不懂的话这玩意最多就只能卖两毛五
    fMonetaryValueAlt: float  # 牌子货？几多钱？(50包邮)如果你认识这东西它的价格则为50
    fDurability: float  # 有没有耐久(改成0就是天顶星黑科技了)
    fDegradePerHour: float  # 每小时耐久消耗(拍一下空格耐久掉多少)
    fEquipDegradePerHour: float  # 如果装备在身上那么该物品每小时消耗多少
    fDegradePerUse: float  # 每次使用消耗的耐久(这里是1,也就是用一次就没了)
    vDegradeTreasureIDs: str  # 当耐久消耗为0时会爆出什么零件
    aEquipConditions: str  # 该物品会为你带来的状态
    aPossessConditions: str  # 该物品会为你带来的永久性状态
    aUseConditions: str  # 使用该物品会为你带来的状态
    aCapacities: str  # 如果该物品是容器的话,那么它的容积是多少
    vEquipSlots: str  # 装备插槽 物品能放在身上位置(位置数同注释2)
    vUseSlots: str  # 能给自己使用的位置(注释3)
    bSocketLocked: bool  # 锁定属性(注释4)
    vProperties: str  # 该物品的属性(结合itemprops数据类别使用、用于合成与检定)
    aContentIDs: str  # 该物品的空间属性(结合containertypes数据类别使用,用于定义该物品作为容器能在内部放置什么东西)
    nFormatID: int  # 该物品内部的战利品池
    nTreasureID: int  # 用于给物品进行大体的分类,结合containertypes数据类别使用
    nComponentID: int  # 成分ID(结合treasuretable数据类别使用)
    bMirrored: bool  # 镜像(专门给鞋子用的)
    nSlotDepth: int  # 未知
    strChargeProfiles: str  # 耗电量
    aAttackModes: str  # 攻击模式
    nStackLimit: int  # 最大堆叠数
    aSwitchIDs: str  # 转变的id(注释5)
    aSounds: str  # 当你拿起放下该物品时的声音


@dataclass
class maps:
    """地图"""

    id: int  # 代码标号
    strName: str  # 调用的图片


@dataclass
class recipes:
    """合成表"""

    nID: int  # 代码标号
    strName: str  # 配方名称【需要翻译】
    strSecretName: str  # 配方的隐藏名称(比如人肉和动物肉,水有没有毒性成分)【需要翻译】
    strTools: str  # 合成需要的工具
    strConsumed: str  # 合成会消耗/损耗掉的物品
    strDestroyed: str  # 摧毁(实际上是用来熄灭火把的)
    nTreasureID: int  # 调用的战利品池(就是你按照上面的合成表合成后能合成出什么玩意)
    fHours: float  # 你合成该项目需要消耗的行动点数
    nReverse: (
        int  # 是否可以逆向工程(比如说衣服拆了就不能再合成回去,而长线和短线可以互相拆分)
    )
    nHiddenID: int  # 是不是隐藏配方(是否只能通过自己摸索或者捡纸片解锁)
    bIdentify: bool  # 是否能被鉴别(一般用于配合隐藏名称)
    bTransferComponents: bool  # 未知
    vAlsoTry: str  # 使用其他不同配方但是却是相同成品的配方的id
    nTempTreasureID: (
        int  # 合成时,在成品栏以虚影显示的合成结果,结合Treasuretable数据类别使用
    )
    bDegradeOutput: (
        bool  # 合成出的物品耐久是否和材料耐久关联 1-有关,0-无关(长矛就是一个例子)
    )
    strType: str  # 合成时的配方类型,不过也可以直接改成合成完的名称【需要翻译】


@dataclass
class treasuretable:
    """战利品池"""

    id: int  # 代码标号
    strName: str  # 战利品名【需要翻译】
    aTreasures: str  # 战利品池的内容(注释1)
    bNested: bool  # 生成物品是否会装在同时生成的容器里
    bSuppress: bool  # 抑制treasuretable内物品可能产生的内容物的生成(若设为1,生成水瓶时瓶子里不会有水。生成枪的时候枪里不会自带子弹)
    bIdentify: bool  # 生成的物品是否被辨识,是否显示隐藏名字。


data_types = [
    "attackmodes",
    "barterhexes",
    "battlemoves",
    "camptypes",
    "chargeprofiles",
    "conditions",
    "containertypes",
    "creatures",
    "creaturesources",
    "datafiles",
    "dmcplaces",
    "encounters",
    "encountertriggers",
    "factions",
    "forbiddenhexes",
    "gamevars",
    "headlines",
    "hextypes",
    "ingredients",
    "itemprops",
    "itemtypes",
    "maps",
    "recipes",
    "treasuretable",
]

translation_name = {
    "strName",
    "strNotes",
    "strWieldPhrase",
    "vAttackPhrases",
    "strSuccess",
    "strFail",
    "strPopUp",
    "strDesc",
    "strNamePublic",
    "strHeadline",
    "strPropertyName",
    "strDescAlt",
    "strSecretName",
    "strType",
}