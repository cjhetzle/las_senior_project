PLANTUML=DISPLAY= plantuml
SRC=$(wildcard *.txt)
DEST=$(SRC:.txt=.png)

main: $(DEST)

%.png: %.txt
	$(PLANTUML) -tpng $^

.PHONY: clean
clean:
	$(RM) $(DEST)
