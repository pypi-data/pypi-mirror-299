from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.publication import Publication
from .comment import (encoder as encoder_1, decoder as decoder_2, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription, ISAJson_encoder as ISAJson_encoder_1)
from .context.rocrate.isa_publication_context import context_jsonvalue
from .decode import (Decode_uri, Decode_noAdditionalProperties)
from .encode import (try_include, try_include_seq)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)
from .person import (ROCrate_encodeAuthorListString, ROCrate_decodeAuthorListString)

__A_ = TypeVar("__A_")

def encoder(oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1849(value: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1848(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1848()

    def _arrow1851(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1850(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr1850()

    def _arrow1853(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1852(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr1852()

    def _arrow1855(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1854(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr1854()

    def _arrow1856(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1859(comment: Comment, oa: Any=oa) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("pubMedID", _arrow1849, oa.PubMedID), try_include("doi", _arrow1851, oa.DOI), try_include("authorList", _arrow1853, oa.Authors), try_include("title", _arrow1855, oa.Title), try_include("status", _arrow1856, oa.Status), try_include_seq("comments", _arrow1859, oa.Comments)]))
    class ObjectExpr1865(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr1865()


def _arrow1876(get: IGetters) -> Publication:
    def _arrow1868(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1869(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1870(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", string)

    def _arrow1872(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1873(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_decoder)

    def _arrow1875(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1868(), _arrow1869(), _arrow1870(), _arrow1872(), _arrow1873(), _arrow1875())


decoder: Decoder_1[Publication] = object(_arrow1876)

def ROCrate_genID(p: Publication) -> str:
    match_value: str | None = p.DOI
    if match_value is None:
        match_value_1: str | None = p.PubMedID
        if match_value_1 is None:
            match_value_2: str | None = p.Title
            if match_value_2 is None:
                return "#EmptyPublication"

            else: 
                return "#Pub_" + replace(match_value_2, " ", "_")


        else: 
            return match_value_1


    else: 
        return match_value



def ROCrate_encoder(oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1883(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr1882(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1882()

    class ObjectExpr1884(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Publication")

    def _arrow1886(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1885(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr1885()

    def _arrow1888(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1887(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr1887()

    def _arrow1889(author_list: str, oa: Any=oa) -> IEncodable:
        return ROCrate_encodeAuthorListString(author_list)

    def _arrow1891(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr1890(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr1890()

    def _arrow1892(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow1893(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow1883()), ("@type", ObjectExpr1884()), try_include("pubMedID", _arrow1886, oa.PubMedID), try_include("doi", _arrow1888, oa.DOI), try_include("authorList", _arrow1889, oa.Authors), try_include("title", _arrow1891, oa.Title), try_include("status", _arrow1892, oa.Status), try_include_seq("comments", _arrow1893, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr1894(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr1894()


def _arrow1901(get: IGetters) -> Publication:
    def _arrow1895(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1896(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1897(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", ROCrate_decodeAuthorListString)

    def _arrow1898(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1899(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow1900(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1895(), _arrow1896(), _arrow1897(), _arrow1898(), _arrow1899(), _arrow1900())


ROCrate_decoder: Decoder_1[Publication] = object(_arrow1901)

def ISAJson_encoder(id_map: Any | None, oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1907(value: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr1906(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1906()

    def _arrow1913(value_2: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr1912(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr1912()

    def _arrow1917(value_4: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr1916(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr1916()

    def _arrow1923(value_6: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr1922(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr1922()

    def _arrow1925(oa_1: OntologyAnnotation, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1927(comment: Comment, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return ISAJson_encoder_1(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("pubMedID", _arrow1907, oa.PubMedID), try_include("doi", _arrow1913, oa.DOI), try_include("authorList", _arrow1917, oa.Authors), try_include("title", _arrow1923, oa.Title), try_include("status", _arrow1925, oa.Status), try_include_seq("comments", _arrow1927, oa.Comments)]))
    class ObjectExpr1934(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], id_map: Any=id_map, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr1934()


ISAJson_allowedFields: FSharpList[str] = of_array(["pubMedID", "doi", "authorList", "title", "status", "comments"])

ISAJson_decoder: Decoder_1[Publication] = Decode_noAdditionalProperties(ISAJson_allowedFields, decoder)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]

