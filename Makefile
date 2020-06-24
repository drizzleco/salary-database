### help - help docs for this Makefile
.PHONY: help
help :
	@sed -n '/^###/p' Makefile

### install - install requirements in venv
.PHONY: install
install:
	#  backend installation
	python3 -m venv .env; \
	. .env/bin/activate; \
	pip install -r requirements.txt;

### collect_data - collect disclosure data and save to db
.PHONY: collect_data
collect_data:
	# just 2019 data for now
	sh data/collect_data.sh disclosure_2019 https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2019/H-1B_Disclosure_Data_FY2019.xlsx

	# sh data/collect_data.sh disclosure_2018 https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Disclosure_Data_FY2018_EOY.xlsx & \
	# sh data/collect_data.sh disclosure_2017 https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Disclosure_Data_FY17.xlsx & \
	# sh data/collect_data.sh disclosure_2016 https://www.foreignlaborcert.doleta.gov/docs/Performance_Data/Disclosure/FY15-FY16/H-1B_Disclosure_Data_FY16.xlsx & \
	# sh data/collect_data.sh disclosure_2015 https://www.foreignlaborcert.doleta.gov/docs/py2015q4/H-1B_Disclosure_Data_FY15_Q4.xlsx & \
	# sh data/collect_data.sh disclosure_2014 https://www.foreignlaborcert.doleta.gov/docs/py2014q4/H-1B_FY14_Q4.xlsx & \
	# sh data/collect_data.sh disclosure_2013 https://www.foreignlaborcert.doleta.gov/docs/lca/LCA_FY2013.xlsx & \
	# sh data/collect_data.sh disclosure_2012 https://www.foreignlaborcert.doleta.gov/docs/py2012_q4/LCA_FY2012_Q4.xlsx & \
	# sh data/collect_data.sh disclosure_2011 https://www.foreignlaborcert.doleta.gov/docs/lca/H-1B_iCert_LCA_FY2011_Q4.xlsx & \
	# sh data/collect_data.sh disclosure_2010 https://www.foreignlaborcert.doleta.gov/docs/lca/H-1B_FY2010.xlsx & \
	# sh data/collect_data.sh disclosure_2009 https://www.foreignlaborcert.doleta.gov/docs/lca/Icert_%20LCA_%20FY2009.xlsx & \
	# sh data/collect_data.sh disclosure_2008 https://www.foreignlaborcert.doleta.gov/docs/lca/H-1B_Case_Data_FY2008.xlsx 
