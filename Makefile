PROTOC = protoc
ANTLR4 := antlr4
CWD := $(shell pwd)
PROTOBUF_SRC := $(CWD)/protobuf
ENTITIES_DIR := $(CWD)/entities
RPC_DIR := $(CWD)/RPC

# Entities Protobuf definitions generation.
# Assumes that Entities Protoc-plugin is installed.
# It is located in "entities/proto/plugins/python".

# Entities: generate test entity-classes for Python.
.PHONY: entities-py-test-proto
entities-py-test-proto:
	$(PROTOC) \
		--proto_path $(PROTOBUF_SRC)/src \
		--proto_path $(ENTITIES_DIR)/proto/ \
		--proto_path $(ENTITIES_DIR)/python/ \
		--python_out $(ENTITIES_DIR)/python/ \
		--entities_out $(ENTITIES_DIR)/python/ \
		$(wildcard $(ENTITIES_DIR)/python/tests/*.proto) $(wildcard $(ENTITIES_DIR)/python/tests/**/*.proto) $(wildcard $(ENTITIES_DIR)/python/tests/**/**/*.proto)

# Entities: generate entity-classes for Python.
.PHONY: entities-py-proto
entities-py-proto:
	$(PROTOC) \
		--proto_path $(PROTOBUF_SRC)/src \
		--proto_path $(ENTITIES_DIR)/proto/ \
		--python_out $(ENTITIES_DIR)/python/src/ \
		--entities_out=$(ENTITIES_DIR)/python/src/ \
		$(wildcard $(ENTITIES_DIR)/proto/*.proto) $(wildcard $(ENTITIES_DIR)/proto/**/*.proto) $(wildcard $(ENTITIES_DIR)/proto/**/**/*.proto)

RPC-py-expressions-parser:
	$(ANTLR4) \
		-visitor \
		-Dlanguage=Python3 \
		-o $(RPC_DIR)/python/src/onedrive_client/RPC/expressions/parser/ \
		$(RPC_DIR)/Expressions.g4
