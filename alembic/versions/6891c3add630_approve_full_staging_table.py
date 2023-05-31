"""approve full staging table

Revision ID: 6891c3add630
Revises: 56969752d52a
Create Date: 2023-05-27 13:35:08.097277

"""
import asyncio
from alembic import op
import sqlalchemy as sa
# from ...core.routers.quote import get_quote_submissions, approve_new_quote


# revision identifiers, used by Alembic.
revision = '6891c3add630'
down_revision = '56969752d52a'
branch_labels = None
depends_on = None

    

def upgrade() -> None:
     op.execute("""
        INSERT INTO quotes_staging (category,quote,author,added_by,date_created,added_to_quotes) VALUES
        ('love','"One forgives to the degree that one loves."','Francois de La Rochefoucauld','automated_py','2023-02-25 23:39:52',0),
        ('love','"The sound of a kiss is not so loud as that of a cannon, but its echo lasts a great deal longer."','Oliver Wendell Holmes, Sr.','automated_py','2023-02-25 23:39:52',0),
        ('love','"A kiss is a rosy dot over the ''i'' of loving."','Cyrano de Bergerac','automated_py','2023-02-25 23:39:52',0),
        ('love','"Love takes up where knowledge leaves off."','Thomas Aquinas','automated_py','2023-02-25 23:39:52',0),
        ('nature','"Twilight drops her curtain down, and pins it with a star."','Lucy Maud Montgomery','automated_py','2023-02-25 23:39:52',0),
        ('nature','"They are ill discoverers that think there is no land, when they can see nothing but sea."','Francis Bacon','automated_py','2023-02-25 23:39:53',0),
        ('nature','"Land is the secure ground of home, the sea is like life, the outside, the unknown."','Stephen Gardiner','automated_py','2023-02-25 23:39:53',0),
        ('nature','"The world is always in movement."','V. S. Naipaul','automated_py','2023-02-25 23:39:53',0),
        ('funny','"If two wrongs don''t make a right, try three."','Laurence J. Peter','automated_py','2023-02-25 23:39:53',0),
        ('funny','"I want my children to have all the things I couldn''t afford. Then I want to move in with them."','Phyllis Diller','automated_py','2023-02-25 23:39:54',0),
        ('funny','"Candy is dandy but liquor is quicker."','Ogden Nash','automated_py','2023-02-25 23:39:54',0),
        ('funny','"An optimist is a fellow who believes a housefly is looking for a way to get out."','George Jean Nathan','automated_py','2023-02-25 23:39:54',0),
        ('art','"I put my heart and my soul into my work, and have lost my mind in the process."','Vincent Van Gogh','automated_py','2023-02-25 23:39:54',0),
        ('art','"I will preach with my brush."','Henry Ossawa Tanner','automated_py','2023-02-25 23:39:54',0),
        ('art','"I have no fear of making changes, destroying the image, etc., because the painting has a life of its own."','Jackson Pollock','automated_py','2023-02-25 23:39:54',0),
        ('art','"When I draw something, the brain and the hands work together."','Tadao Ando','automated_py','2023-02-25 23:39:54',0),
        ('love','"Love possesses not nor will it be possessed, for love is sufficient unto love."','Khalil Gibran','automated_py','2023-02-27 02:36:55',0),
        ('love','"One forgives to the degree that one loves."','Francois de La Rochefoucauld','automated_py','2023-02-27 02:36:55',0),
        ('love','"The sound of a kiss is not so loud as that of a cannon, but its echo lasts a great deal longer."','Oliver Wendell Holmes, Sr.','automated_py','2023-02-27 02:36:55',0),
        ('love','"A kiss is a rosy dot over the ''i'' of loving."','Cyrano de Bergerac','automated_py','2023-02-27 02:36:56',0),
        ('nature','"Consider what each soil will bear, and what each refuses."','Virgil','automated_py','2023-02-27 02:36:58',0),
        ('nature','"Twilight drops her curtain down, and pins it with a star."','Lucy Maud Montgomery','automated_py','2023-02-27 02:36:58',0),
        ('nature','"They are ill discoverers that think there is no land, when they can see nothing but sea."','Francis Bacon','automated_py','2023-02-27 02:36:58',0),
        ('nature','"Land is the secure ground of home, the sea is like life, the outside, the unknown."','Stephen Gardiner','automated_py','2023-02-27 02:36:58',0),
        ('funny','"Weather forecast for tonight: dark."','George Carlin','automated_py','2023-02-27 02:37:05',0),
        ('funny','"If two wrongs don''t make a right, try three."','Laurence J. Peter','automated_py','2023-02-27 02:37:05',0),
        ('funny','"I want my children to have all the things I couldn''t afford. Then I want to move in with them."','Phyllis Diller','automated_py','2023-02-27 02:37:05',0),
        ('funny','"Candy is dandy but liquor is quicker."','Ogden Nash','automated_py','2023-02-27 02:37:05',0),
        ('art','"With color one obtains an energy that seems to stem from witchcraft."','Henri Matisse','automated_py','2023-02-27 02:37:08',0),
        ('art','"I put my heart and my soul into my work, and have lost my mind in the process."','Vincent Van Gogh','automated_py','2023-02-27 02:37:08',0),
        ('art','"I will preach with my brush."','Henry Ossawa Tanner','automated_py','2023-02-27 02:37:08',0),
        ('art','"I have no fear of making changes, destroying the image, etc., because the painting has a life of its own."','Jackson Pollock','automated_py','2023-02-27 02:37:08',0),
        ('love','"I think you have to pay for love with bitter tears."','Edith Piaf','automated_py','2023-02-28 04:53:44',0),
        ('love','"Love possesses not nor will it be possessed, for love is sufficient unto love."','Khalil Gibran','automated_py','2023-02-28 04:53:44',0),
        ('love','"One forgives to the degree that one loves."','Francois de La Rochefoucauld','automated_py','2023-02-28 04:53:44',0),
        ('love','"The sound of a kiss is not so loud as that of a cannon, but its echo lasts a great deal longer."','Oliver Wendell Holmes, Sr.','automated_py','2023-02-28 04:53:44',0),
        ('nature','"The Sun, Moon and Stars are there to guide us."','Dennis Banks','automated_py','2023-02-28 04:53:44',0),
        ('nature','"Consider what each soil will bear, and what each refuses."','Virgil','automated_py','2023-02-28 04:53:44',0),
        ('nature','"Twilight drops her curtain down, and pins it with a star."','Lucy Maud Montgomery','automated_py','2023-02-28 04:53:44',0),
        ('nature','"They are ill discoverers that think there is no land, when they can see nothing but sea."','Francis Bacon','automated_py','2023-02-28 04:53:45',0),
        ('funny','"Never get a mime talking. He won''t stop."','Marcel Marceau','automated_py','2023-02-28 04:53:45',0),
        ('funny','"Weather forecast for tonight: dark."','George Carlin','automated_py','2023-02-28 04:53:45',0),
        ('funny','"If two wrongs don''t make a right, try three."','Laurence J. Peter','automated_py','2023-02-28 04:53:45',0),
        ('funny','"I want my children to have all the things I couldn''t afford. Then I want to move in with them."','Phyllis Diller','automated_py','2023-02-28 04:53:45',0),
        ('art','"I paint as if I were Rothschild."','Paul Cezanne','automated_py','2023-02-28 04:53:46',0),
        ('art','"With color one obtains an energy that seems to stem from witchcraft."','Henri Matisse','automated_py','2023-02-28 04:53:46',0),
        ('art','"I put my heart and my soul into my work, and have lost my mind in the process."','Vincent Van Gogh','automated_py','2023-02-28 04:53:46',0),
        ('art','"I will preach with my brush."','Henry Ossawa Tanner','automated_py','2023-02-28 04:53:46',0);
        """)


def downgrade() -> None:
    pass
