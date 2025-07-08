from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'qa',
        sa.Column('q_id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('question', sa.Text, nullable=False),
        sa.Column('answer', sa.Text, nullable=False),
        sa.Column('pdf_url', sa.String, nullable=True),
    )
    op.create_table(
        'search_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_query', sa.Text),
        sa.Column('candidates', sa.Text),
        sa.Column('selected_q2', sa.Text, nullable=True),
        sa.Column('topk', sa.Integer),
    )

def downgrade():
    op.drop_table('search_log')
    op.drop_table('qa')
