# CSharp MySQL Skill

此 skill 提取 C# 代码层面与 MySQL 数据访问相关的实现模板，避免语言混淆，专注于 C# 与 MySQL 的联合代码实现。

## 代码责任边界

- 仅处理 C# 代码实现层面
- 包括数据库连接、DatabaseManager、实体类、Repository、事务与查询模式
- 不涉及 SQL 方言以外的业务架构设计

## 核心模板

### C# 数据库连接初始化

```csharp
var connStr = "Server=127.0.0.1;Port=3306;Database={DbName};User ID=root;Password=yourpwd;CharSet=utf8mb4;";

using var connection = CreateConnection(connStr);
connection.Open();
```

### DatabaseManager（建库 + 建表）

```csharp
public class DatabaseManager {
    private readonly IDbConnection _connection;
    private readonly string _serverConnStr;

    public DatabaseManager(string connStr) {
        _connection = CreateConnection(connStr);
        _serverConnStr = RemoveDatabaseSegment(connStr) + "Database=mysql;";
    }

    public async Task CreateDatabaseIfNotExistsAsync(string dbName) {
        using var connection = CreateConnection(_serverConnStr);
        await connection.ExecuteAsync(
            $"CREATE DATABASE IF NOT EXISTS `{dbName}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;");
    }

    public void SyncTable<TTable>() where TTable : class {
        // 使用项目已选的 ORM/迁移工具同步表结构
    }

    private IDbConnection CreateConnection(string connStr) {
        // 根据项目环境创建数据库连接对象
        throw new NotImplementedException();
    }

    private string RemoveDatabaseSegment(string connStr) {
        // 移除连接串中的 Database= 段
        throw new NotImplementedException();
    }
}
```

### 实体类模板

```csharp
[Table(Name = "{TableName}")]
public class {Table} {
    [Column(IsPrimary = true, IsIdentity = true)]
    public long Id { get; set; }

    [Column(StringLength = 128, IsNullable = false)]
    public string Name { get; set; } = string.Empty;

    [Column(IsNullable = true)]
    public string? Description { get; set; }

    [Column(ServerTime = DateTimeKind.Utc, CanUpdate = false)]
    public DateTime CreatedAt { get; set; }

    [Column(ServerTime = DateTimeKind.Utc)]
    public DateTime UpdatedAt { get; set; }
}
```

### Repository 模板

```csharp
public class {Table}Repository {
    private readonly IGenericRepository<{Table}> _repo;

    public {Table}Repository(IGenericRepository<{Table}> repo) {
        _repo = repo;
    }

    public Task<{Table}?> GetByIdAsync(long id) =>
        _repo.Where(e => e.Id == id).FirstAsync();

    public Task<List<{Table}>> GetAllAsync() =>
        _repo.Select.ToListAsync();

    public async Task<{Table}> CreateAsync({Table} table) {
        await _repo.InsertAsync(table);
        return table;
    }

    public Task UpdateAsync({Table} table) =>
        _repo.UpdateAsync(table);

    public Task DeleteAsync(long id) =>
        _repo.DeleteAsync(e => e.Id == id);
}
```

### 事务与查询模式

```csharp
using var uow = unitOfWorkFactory.Create();
var repoA = uow.GetRepository<TableA>();
var repoB = uow.GetRepository<TableB>();

await repoA.InsertAsync(a);
await repoB.InsertAsync(b);

uow.Commit();
```

```csharp
var list = await repo.Select
    .Where(e => e.Name.Contains(keyword))
    .OrderByDescending(e => e.CreatedAt)
    .Page(pageIndex, pageSize)
    .ToListAsync();
```

```csharp
var result = await repo.Select<OrderTable, UserTable>()
    .LeftJoin((o, u) => o.UserId == u.Id)
    .Where((o, u) => u.IsActive)
    .ToListAsync((o, u) => new { o.Id, u.Name });
```

## 约束

- 代码实现必须是 C# 风格，避免语言混淆。
- 如果涉及 SQL 或数据库访问逻辑，应使用项目当前选定的 ORM 或数据库访问层。
- 采用中文交流。
