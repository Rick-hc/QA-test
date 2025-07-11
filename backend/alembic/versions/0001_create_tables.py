from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'qa',
        sa.Column('q_id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('question', sa.Text, nullable=False),
        sa.Column('answer', sa.Text, nullable=False),
        sa.Column('pdf_url', sa.String, nullable=True),
    )
    op.create_table(
        'search_log',
        sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('user_query', sa.Text, nullable=False),
        sa.Column('q1_list', sa.Text, nullable=False),
        sa.Column('selected_q2', sa.Text, nullable=True),
        sa.Column('topk', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

def downgrade() -> None:
    op.drop_table('search_log')
    op.drop_table('qa')
