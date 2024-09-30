import pandas as pd
from pydantic import BaseModel, Field, PositiveInt, model_validator
from typing import Optional, Dict, List, Self, Any
from enum import Enum



class QType(str, Enum):
    SA = 'SA'
    MA = 'MA'
    NUM = 'NUM'
    FT = 'FT'
    SA_MTR = 'SA_mtr'
    MA_MTR = 'MA_mtr'



class NumAtt(str, Enum):
    MEAN = 'mean'
    STD = 'std'
    MIN = 'min'
    MAX = 'max'
    _25 = '25%'
    _50 = '50%'
    _75 = '75%'



class CatAtt(BaseModel):
    code: str = Field(min_length=1, frozen=True)
    label: str = Field(min_length=1, frozen=True)

    factor: Optional[int | float] = Field(default=None)

    group_stt: Optional[str] = Field(default=None, pattern=r'combine|net')
    group_code: Optional[dict] = Field(default=None)





class Question(BaseModel):

    def __init__(self, /, **data: Any):
        super().__init__(**data)


    name: str = Field(min_length=2, frozen=True)
    label: Optional[str] = Field(min_length=2, default=None)
    type: Optional[QType] = Field(default=None)
    cols: Optional[List[str]] = Field(default=None)

    obj_cats: Optional[List[CatAtt]] = Field(default=None)
    obj_num: Optional[List[NumAtt]] = Field(default=None)

    cats: Optional[Dict[str | int, str | dict]] = Field(default=None)
    mean_factor: Optional[Dict[PositiveInt, float]] = Field(default=None)

    filter: Optional[str] = Field(default=None)
    sort: Optional[str] = Field(default=None, pattern=r'acs|des')
    calculation: Optional[Dict[str, str]] = Field(default=None, examples=[{"lbl": "Sum(T2B, B2B)", "syntax": "[T2B] + [B2B]"}])


    def fill_question(self, df_qre: pd.DataFrame) -> Self:

        # LABEL --------------------------------------------------------------------------------------------------------
        if self.label is None:
            self.label = df_qre['var_lbl'].values[0]

        elif '{lbl}' in self.label:
            self.label = self.label.replace('{lbl}', df_qre['var_lbl'].values[0])


        # TYPE ---------------------------------------------------------------------------------------------------------
        self.type = df_qre['var_type'].values[0]

        # COLUMNS ------------------------------------------------------------------------------------------------------
        self.cols = df_qre['var_name'].values.tolist()


        # CATEGORICAL ATTRIBUTES ---------------------------------------------------------------------------------------
        # MEAN FACTOR ---------------------------------------------------------------------------------------

        if self.cats is None:
            self.cats = df_qre['val_lbl'].values[0]

        if (self.type not in [QType.SA, QType.SA_MTR]) and self.mean_factor is not None:
            raise ValueError(f"Attribute 'mean_factor' only use for SA question!!!")

        if self.type in [QType.SA, QType.SA_MTR, QType.MA, QType.MA_MTR]:
            self.obj_cats: List[CatAtt] = list()

            for code, label in self.cats.items():
                self.find_cat(code, label, self.mean_factor)











        if self.type != QType.NUM and self.obj_num is not None:
            raise ValueError(f"Attribute 'num_att' only use for NUM question!!!")



        return self



    def find_cat(self, code, label, mean_factor):

        if code == 'net_code':

            for code2, label2 in label.items():

                if isinstance(label2, dict) and '|' in code2:

                    code3, group_stt, label3 = str(code2).split('|')

                    self.obj_cats.append(CatAtt(
                        code=code3, label=label3, factor=mean_factor.get(int(code3)) if mean_factor else None,
                        group_stt=group_stt, group_code=label2
                    ))

                else:
                    self.find_cat(code2, label2, mean_factor)


        else:

            if isinstance(label, dict) and '|' in code:
                code3, group_stt, label3 = str(code).split('|')

                self.obj_cats.append(CatAtt(
                    code=code3, label=label3, factor=mean_factor.get(int(code3)) if mean_factor else None,
                    group_stt=group_stt, group_code=label
                ))

            else:
                self.obj_cats.append(CatAtt(code=code, label=label, factor=mean_factor.get(int(code)) if mean_factor else None))


