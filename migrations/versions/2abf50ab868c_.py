"""empty message

Revision ID: 2abf50ab868c
Revises: 
Create Date: 2024-09-06 10:43:58.107740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2abf50ab868c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agelimit',
    sa.Column('AgeLimitID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AgeLimit', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('AgeLimitID')
    )
    op.create_table('calendar2024',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('day')
    )
    op.create_table('discount',
    sa.Column('DiscountID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('DiscountName', sa.String(length=30), nullable=True),
    sa.Column('Discount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('DiscountID')
    )
    op.create_table('moviecategory',
    sa.Column('MovieCategoryID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CategoryName', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('MovieCategoryID')
    )
    op.create_table('price',
    sa.Column('PriceID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('PricePlans', sa.String(length=20), nullable=True),
    sa.Column('Price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('PriceID')
    )
    op.create_table('screen',
    sa.Column('ScreenID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ScreenID')
    )
    op.create_table('sex',
    sa.Column('SexID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Sex', sa.String(length=4), nullable=True),
    sa.PrimaryKeyConstraint('SexID')
    )
    op.create_table('showtime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kubunmei', sa.String(length=80), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('account',
    sa.Column('AccountID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AccountNumber', sa.String(length=8), nullable=True),
    sa.Column('Name', sa.String(length=50), nullable=True),
    sa.Column('KanaName', sa.String(length=50), nullable=True),
    sa.Column('SexID', sa.Integer(), nullable=True),
    sa.Column('Password', sa.String(length=12), nullable=True),
    sa.Column('MailAddress', sa.String(length=255), nullable=True),
    sa.Column('PhoneNumber', sa.String(length=13), nullable=True),
    sa.Column('Birthday', sa.Date(), nullable=True),
    sa.Column('MemberFlg', sa.Boolean(create_constraint=1), server_default='0', nullable=True),
    sa.Column('RegistDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['SexID'], ['sex.SexID'], ),
    sa.PrimaryKeyConstraint('AccountID')
    )
    op.create_table('movie',
    sa.Column('MovieID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('MovieTitle', sa.String(length=50), nullable=True),
    sa.Column('AgeLimitID', sa.Integer(), nullable=True),
    sa.Column('MovieCategoryID', sa.Integer(), nullable=True),
    sa.Column('PriceID', sa.Integer(), nullable=True),
    sa.Column('MD', sa.String(length=50), nullable=True),
    sa.Column('MS', sa.String(length=50), nullable=True),
    sa.Column('Overview', sa.String(length=2000), nullable=True),
    sa.Column('ShowTimes', sa.Integer(), nullable=True),
    sa.Column('StartDate', sa.Integer(), nullable=True),
    sa.Column('FinishDate', sa.Integer(), nullable=True),
    sa.Column('MovieImageLength', sa.String(length=255), nullable=True),
    sa.Column('MovieImageSide', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['AgeLimitID'], ['agelimit.AgeLimitID'], ),
    sa.ForeignKeyConstraint(['FinishDate'], ['calendar2024.id'], ),
    sa.ForeignKeyConstraint(['MovieCategoryID'], ['moviecategory.MovieCategoryID'], ),
    sa.ForeignKeyConstraint(['PriceID'], ['price.PriceID'], ),
    sa.ForeignKeyConstraint(['StartDate'], ['calendar2024.id'], ),
    sa.PrimaryKeyConstraint('MovieID')
    )
    op.create_table('seat',
    sa.Column('SeatID', sa.Integer(), nullable=False),
    sa.Column('Row', sa.String(length=1), nullable=False),
    sa.Column('Number', sa.Integer(), nullable=False),
    sa.Column('ScreenID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ScreenID'], ['screen.ScreenID'], ),
    sa.PrimaryKeyConstraint('SeatID')
    )
    op.create_table('address',
    sa.Column('AddressID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('PostNumber', sa.String(length=8), nullable=True),
    sa.Column('Todohuken', sa.String(length=8), nullable=True),
    sa.Column('Shiku', sa.String(length=20), nullable=True),
    sa.Column('ChosonNumber', sa.String(length=255), nullable=True),
    sa.Column('AccountID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AccountID'], ['account.AccountID'], ),
    sa.PrimaryKeyConstraint('AddressID')
    )
    op.create_table('cast',
    sa.Column('CastD', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CastName', sa.String(length=100), nullable=True),
    sa.Column('MovieID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['MovieID'], ['movie.MovieID'], ),
    sa.PrimaryKeyConstraint('CastD')
    )
    op.create_table('showing',
    sa.Column('ShowingID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ShowDate', sa.Integer(), nullable=True),
    sa.Column('ShowTime', sa.Integer(), nullable=True),
    sa.Column('MovieID', sa.Integer(), nullable=True),
    sa.Column('ScreenID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['MovieID'], ['movie.MovieID'], ),
    sa.ForeignKeyConstraint(['ScreenID'], ['screen.ScreenID'], ),
    sa.ForeignKeyConstraint(['ShowDate'], ['calendar2024.id'], ),
    sa.ForeignKeyConstraint(['ShowTime'], ['showtime.id'], ),
    sa.PrimaryKeyConstraint('ShowingID')
    )
    op.create_table('reservation',
    sa.Column('ReservationID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AccountID', sa.Integer(), nullable=True),
    sa.Column('ShowingID', sa.Integer(), nullable=True),
    sa.Column('DiscountID', sa.Integer(), nullable=True),
    sa.Column('otona', sa.Integer(), nullable=True),
    sa.Column('kodomo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AccountID'], ['account.AccountID'], ),
    sa.ForeignKeyConstraint(['DiscountID'], ['discount.DiscountID'], ),
    sa.ForeignKeyConstraint(['ShowingID'], ['showing.ShowingID'], ),
    sa.PrimaryKeyConstraint('ReservationID')
    )
    op.create_table('reservseat',
    sa.Column('ReservSeatID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ReservationID', sa.Integer(), nullable=True),
    sa.Column('SeatID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ReservationID'], ['reservation.ReservationID'], ),
    sa.ForeignKeyConstraint(['SeatID'], ['seat.SeatID'], ),
    sa.PrimaryKeyConstraint('ReservSeatID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservseat')
    op.drop_table('reservation')
    op.drop_table('showing')
    op.drop_table('cast')
    op.drop_table('address')
    op.drop_table('seat')
    op.drop_table('movie')
    op.drop_table('account')
    op.drop_table('showtime')
    op.drop_table('sex')
    op.drop_table('screen')
    op.drop_table('price')
    op.drop_table('moviecategory')
    op.drop_table('discount')
    op.drop_table('calendar2024')
    op.drop_table('agelimit')
    # ### end Alembic commands ###
