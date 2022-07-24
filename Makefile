.PHONY: build_uis

build_uis:
	pyuic6 ui/static/main.ui -o ui/generated/main.py ;\
	pyuic6 ui/static/single_phase.ui -o ui/generated/single_phase.py ;\
	pyuic6 ui/static/several_phases.ui -o ui/generated/several_phases.py ;\
	pyuic6 ui/static/regular_polygon.ui -o ui/generated/regular_polygon.py ;\
	pyuic6 ui/static/single_several.ui -o ui/generated/single_several.py ;\
