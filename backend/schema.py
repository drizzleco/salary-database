import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db, Salary as SalaryModel


class Salary(SQLAlchemyObjectType):
    """
    Salary Model
    """

    class Meta:
        model = SalaryModel


class Query(graphene.ObjectType):
    """
    Base Query
    """

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
                db.or_(SalaryModel.employer_name.like(fuzzy_query["employer"])),
                db.or_(SalaryModel.job_title.like(fuzzy_query["title"])),
                db.or_(SalaryModel.employer_city.like(fuzzy_query["city"])),
                db.or_(SalaryModel.employer_state.like(fuzzy_query["state"])),
                db.or_(
                    db.func.substr(SalaryModel.employment_start_date, -2).like(year)
                ),
            )
            .offset(offset)
            .limit(page_size)
        )


schema = graphene.Schema(query=Query)
