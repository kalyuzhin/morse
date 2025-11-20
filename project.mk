CURRENT_DIR=$(shell pwd)
PROTO_DIR=$(CURRENT_DIR)/api
PROTO_FILE=$(PROTO_DIR)/morse.proto
PB_DIR=$(CURRENT_DIR)/pb

.PHONY: help
## prints help about all targets
help:
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@awk '                                \
		BEGIN { comment=""; }             \
		/^\s*##/ {                         \
		    comment = substr($$0, index($$0,$$2)); next; \
		}                                  \
		/^[a-zA-Z0-9_-]+:/ {               \
		    target = $$1;                  \
		    sub(":", "", target);          \
		    if (comment != "") {           \
		        printf "  %-17s %s\n", target, comment; \
		        comment="";                \
		    }                              \
		}' $(MAKEFILE_LIST)
	@echo ""

.PHONY: proto-gen
## generate proto files
proto-gen:
	mkdir $(PB_DIR)
	python -m grpc_tools.protoc -I $(PROTO_DIR) $(PROTO_FILE) --python_out=$(PB_DIR) --pyi_out=$(PB_DIR) --grpc_python_out=$(PB_DIR)