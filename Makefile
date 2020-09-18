.PHONY: build_uis

build_uis:
	pyuic5 ui/static/main.ui -o ui/generated/main.py ;\
	pyuic5 ui/static/single_phase.ui -o ui/generated/single_phase.py ;\
	pyuic5 ui/static/several_phases.ui -o ui/generated/several_phases.py ;\
	pyuic5 ui/static/regular_polygon.ui -o ui/generated/regular_polygon.py ;\
	pyuic5 ui/static/single_several.ui -o ui/generated/single_several.py ;\
