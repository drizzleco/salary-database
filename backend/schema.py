import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db, Salary as SalaryModel


class Salary(SQLAlchemyObjectType):
    class Meta:
        model = SalaryModel


class Query(graphene.ObjectType):
    salaries = graphene.List(
        Salary,
        employer=graphene.String(),
        title=graphene.String(),
        city=graphene.String(),
        state=graphene.String(),
        year=graphene.String(),
        page=graphene.Int(),
        limit=graphene.Int(),
    )

    def resolve_salaries(self, info, **args):
        page_size = args.get("limit", 10)
        offset = args.get("page", 0) * page_size
        fuzzy_query = {}
        for query in ["employer", "title", "city", "state"]:
            fuzzy_query[query] = "%{}%".format(args.get(query, ""))
        year = args.get("year")
        year = year[-2:] if year else "%%"  # get year without century
        return (
            Salary.get_query(info)
            .filter(
                db.or_(SalaryModel.EMPLOYER_NAME.like(fuzzy_query["employer"])),
                db.or_(SalaryModel.JOB_TITLE.like(fuzzy_query["title"])),
                db.or_(SalaryModel.EMPLOYER_CITY.like(fuzzy_query["city"])),
                db.or_(SalaryModel.EMPLOYER_STATE.like(fuzzy_query["state"])),
                db.or_(
                    db.func.substr(SalaryModel.EMPLOYMENT_START_DATE, -2).like(year)
                ),
            )
            .offset(offset)
            .limit(page_size)
        )


schema = graphene.Schema(query=Query)
