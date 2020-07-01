import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db, Salary as SalaryModel


class Salary(SQLAlchemyObjectType):
    class Meta:
        model = SalaryModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    salaries = SQLAlchemyConnectionField(
        Salary,
        employer=graphene.String(),
        title=graphene.String(),
        city=graphene.String(),
        state=graphene.String(),
    )

    def resolve_salaries(self, info, **args):
        fuzzy_query = {}
        for query in ["employer", "title", "city", "state"]:
            fuzzy_query[query] = "%{}%".format(args.get(query, ""))
        matched = Salary.get_query(info).filter(
            db.or_(SalaryModel.EMPLOYER_NAME.like(fuzzy_query["employer"])),
            db.or_(SalaryModel.JOB_TITLE.like(fuzzy_query["title"])),
            db.or_(SalaryModel.EMPLOYER_CITY.like(fuzzy_query["city"])),
            db.or_(SalaryModel.EMPLOYER_STATE.like(fuzzy_query["state"])),
            # db.or_(Salary.year == int(session.get("year"))),  # this doesn't work
        )
        return matched.all()


schema = graphene.Schema(query=Query)
