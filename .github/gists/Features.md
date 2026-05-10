# Features
以关键Function、Typedef、配置为记录条目:
- enum: 枚举
- st: class/struct 类型
- ns: 静态函数
- f: function 函数
- as: Asset 资源

## Runtime
### Typedef
[x] enum EntityType
[x] st TypeID
[x] st UniqueID
[x] st Vector2Short

### Module
- st AssetModule
    [x] f Role_TryGet
    [x] f Cell_TryGet
    [x] f Road_TryGet
    [x] f Landscape_TryGet

### Controller
- ns MissionController
- ns RoleController
    [x] f Spawn
    [x] f Unspawn
- ns CellController
    [x] f Spawn
    [x] f Unspawn
- ns RoadController
    [x] f Spawn
    [x] f Unspawn
- ns LandscapeController
    [x] f Spawn
    [x] f Unspawn

### Entity
- st UserEntity
    [x] st UserEntity
    [x] st UserIDComponent
- st MissionEntity
    [x] st MissionSO
- st RoleEntity
    [x] st RoleEntity
    [x] st RoleRepository
    [x] st RoleSO
- st CellEntity
    [x] st CellSpawner
    [x] st CellEntity
    [x] st CellRepository
    [x] st CellSO
    [x] enum CellType
- st RoadEntity
    [x] st RoadSpawner
    [x] st RoadEntity
    [x] st RoadRepository
    [x] st RoadSO
    [x] enum RoadType
- st LandscapeEntity
    [x] st LandscapeEntity
    [x] st LandscapeRepository
    [x] st LandscapeSO
    [x] st LandscapeSpawner
    [x] enum LandscapeType

## Editor
### EM
- st MissionSpawnerEM
    [x] f Bake
    [x] f Rename
- st CellSpawnerEM
    [x] f Bake
    [x] f Rename
    [x] f OnDrawGizmos
- st RoadSpawnerEM
    [x] f Bake
    [x] f Rename
    [x] f OnDrawGizmos
- st LandscapeSpawnerEM
    [x] f Bake
    [x] f Rename