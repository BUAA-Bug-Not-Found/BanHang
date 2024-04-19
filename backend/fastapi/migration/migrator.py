# 生产环境可能需要migration，
# 当前由于没有有价值数据，且多人同时mergemigration会冲突，
# 故暂时不启用

from peewee_migrate import Router
import orm.orm as model

model.db.connect()
router = Router(model.db)

# Create migration
router.create(auto=model)

# Run migration/migrations
router.run('migration_name')

# Run all unapplied migrations
router.run()
db.close()

